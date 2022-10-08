from tkinter import filedialog
from tkinter import messagebox
import os, json, xmltodict, requests, plistlib, zlib, io, tarfile, zipfile

decryptapi = "http://server_ip/phi_decrypt/"

def mkdir(path):
    path = path.strip()
    path = path.rstrip("\\")
    isExists = os.path.exists(path)
    if not isExists:
        os.makedirs(path)
        return True
    else:
        return False

def adb_devices():
    tmp = []
    out = os.popen(r"res\platform-tools\adb.exe devices").read()
    spilted = out.split('\n')
    del spilted[0]
    spilted.pop()
    spilted.pop()
    for item in spilted:
        tmp.append(item.split('\t'))
    return tmp

def SearchFiles(directory, fileType):      
    fileList=[]    
    for root, subDirs, files in os.walk(directory):
        for fileName in files:
            if fileName.endswith(fileType):
                fileList.append(os.path.join(root,fileName))
    return fileList

def xmldecrypt(xmlpath: str):
    with open(xmlpath) as fd:
        raw = xmltodict.parse(fd.read())
    raw["FileType"] = "xml"
    a = requests.post(decryptapi, json = raw)
    data = a.content.decode('utf-8')
    data = json.loads(data)
    return data

def is_base64_code(s):
    try:
        _base64_code = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I',
                        'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
                        'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a',
                        'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j',
                        'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's',
                        't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1',
                        '2', '3', '4', '5', '6', '7', '8', '9', '+',
                        '/', '=']
        _base64_code_set = set(_base64_code)
        code_fail = [i for i in s if i not in _base64_code_set]
        if code_fail or len(s) % 4 != 0:
            return False
        return True
    except:
        return False

def abdecrypt(abpath: str, qqid: str):
    mkdir("tmp")
    with open(abpath, 'rb') as f:
        f.seek(24)  # skip 24 bytes
        data = f.read()  # read the rest

        tarstream = zlib.decompress(data)
        file = tarfile.open(fileobj=io.BytesIO(tarstream))

        namelist = []
        for i in file.getmembers():
            namelist.append(i.name)
    
        for i in namelist:
            if(i.endswith("com.PigeonGames.Phigros.v2.playerprefs.xml")):
                xml_path = i
                break
        
        if(xml_path != "None"):
            file.extract(xml_path, "tmp")
            xml_path = 'tmp/' + xml_path
        else:
            messagebox.showinfo('提示', '未在存档文件中找到playerprefs.xml\n请检查备份步骤并重试')
        file.close()
    return xmldecrypt(xml_path, qqid)

def plisttodict(plistpath: str):
    plist = plistlib.load(open(plistpath, "rb"))
    raw = {}
    raw["FileType"] = "plist"
    raw["map"] = {}
    raw["map"]["int"] = {}
    raw['map']['string'] = dict(plist)
    key_list = plist.keys()
    for i in key_list:
        try:
            raw['map']['string'][i] = raw['map']['string'][i].decode('utf-8')
            try:
                raw['map']['string'][i] = json.loads(raw['map']['string'][i])
            except:
                continue
        except:
            continue
    key_list = plist.keys()
    for i in key_list:
        if(not (is_base64_code(i) and is_base64_code(raw['map']['string'][i]))):
            if(i != "password"):
                raw["map"]["int"][i] = raw['map']['string'][i]
            del raw['map']['string'][i]
    return raw

def plistdecrypt(plistpath: str, qqid: str):
    raw = plisttodict(plistpath)
    a = requests.post(decryptapi, json = raw)
    data = a.content.decode('utf-8')
    data = json.loads(data)
    # print(data)
    return data

if __name__=='__main__':
    filename = filedialog.askopenfilename(filetypes=[('Phigros存档文件',('.xml', '.plist', '.ab'))])
    if(filename.endswith(".xml")):
        archive = xmldecrypt(filename)
    elif(filename.endswith(".plist")):
        archive = plistdecrypt(filename)
    elif(filename.endswith(".ab")):
        archive = abdecrypt(filename)
    with open("decrypted.json", 'w', encoding='utf-8') as f:
        json.dump(archive, f, indent=4, ensure_ascii=False)
    print("存档解密完成")
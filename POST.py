import requests, json
import xmltodict

if __name__=="__main__":
    with open("test.xml") as fd:
        raw = xmltodict.parse(fd.read())
    a = requests.post("http://server_ip/phi_decrypt/", json = raw)
    data = a.content.decode('utf-8')
    data = json.loads(data)
    # print(data)
    with open("decrypted.json", 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
# PhiCrypto
 Phigros存档解密API及请求方法实例

# 注：本项目目前已停止服务

# 返回值说明
 `status` 有`True`和`False`两种值，表示是否成功解码

 `playerid` 代表存档内玩家名

 `challengemoderank` 代表课题模式成绩，其中后两位是课题等级，第一位是课题等级颜色，如345是红45，548是彩48

 **`scores`** key为歌曲`songId`+`难度`

 `s`,`a`,`c`分别代表`分数`，`acc`，`是否全连(1为全连，0为非全连)`
 
 `rks_m`代表rks倍率，乘以单曲定数即为单曲rks

 **关于服务器IP**

  POST.py中需要替换`server_ip`，ip可前往主播的b站：[yuhao7370](https://space.bilibili.com/275661582) 私信获取


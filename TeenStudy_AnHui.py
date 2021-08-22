# -*- coding:utf-8 -*-
import requests, xlrd, smtplib
from urllib.parse import urlencode
from email.mime.text import MIMEText

# UrlEncode编码 和 UrlDecode解码


def InitEmailInfo():
    wb = xlrd.open_workbook('InfoFile/Email.xlsx')    # 打开excel
    sh = wb.sheet_by_name('Sheet1')     # 按工作簿定位工作表
    AllList = []
    numList = []
    for i in range(1, sh.nrows):
        listTemp = [sh.row_values(i)[0], sh.row_values(i)[1]]
        AllList.append(listTemp)
        numList.append(sh.row_values(i)[0])
    print(AllList)
    return AllList


def GetNewTableName():  # 获取最新一期的青年大学习
    RankRsp = requests.get("http://dxx.ahyouth.org.cn/api/peopleRankList")
    RankJson = RankRsp.json()
    return RankJson['list'][0]['table_name']


def Send_Email():
    msg = MIMEText('青年大学习！不用回复！赶紧做！！')  # 构造邮件，内容为青年大学习
    msg["Subject"] = "青年大学习！！又是你！！！"  # 设置邮件主题
    msg["From"] = '辛苦勤奋艰苦奋斗的团支书'  # 寄件者
    msg["To"] = '未做人员'              # 收件者
    from_addr = ''      # TODO 这里记得写你的邮箱地址
    password = ''       # TODO 这里记得更改上面为from_addr的邮箱的申请码
    smtp_server = 'smtp.qq.com'  # smtp服务器地址
    to_addr = GetNotFinishList()  # 收件人地址
    print(to_addr)
    try:
        # smtp协议的默认端口是25，QQ邮箱smtp服务器端口是465,第一个参数是smtp服务器地址，第二个参数是端口，第三个参数是超时设置,这里必须使用ssl证书，要不链接不上服务器
        server = smtplib.SMTP_SSL(smtp_server, 465, timeout=2)
        server.login(from_addr, password)  # 登录邮箱
        # 发送邮件，第一个参数是发送方地址，第二个参数是接收方列表，列表中可以有多个接收方地址，表示发送给多个邮箱，msg.as_string()将MIMEText对象转化成文本
        server.sendmail(from_addr, to_addr, msg.as_string())
        server.quit()
        print('发送邮件成功')
    except Exception as e:
        print('发送邮件失败: ', e)


def GetNotFinishList():  # 获取名单
    ClassAllListEmail = [['黄芳丽', '2762179613@qq.com'], ['柳长晶', '630970316@qq.com'], ['王琴', '3600819080@qq.com'],
         ['武添畅', '2552623991@qq.com'], ['李宇桐', '1767993951@qq.com'], ['王阿丽', '2472212957@qq.com'],
         ['张玉婷', '2367070891@qq.com'], ['杨丹', '2835844506@qq.com'], ['张晓雪', '1903811279@qq.com'],
         ['宋真彦', '3083259139@qq.com'], ['邓雅梅', '2291795488@qq.com'], ['陈少云', '2047926209@qq.com'],
         ['张鸿琳', '1695184801@qq.com'], ['陈晨', '2287493223@qq.com'], ['张义', '1832712425@qq.com'],
         ['方霖', '1219676238@qq.com'], ['赵远', '1335400482@qq.com'], ['姜宇', '920918515@qq.com'],
         ['赵仕程', '1481183054@qq.com'], ['刘强', '1481183054@qq.com'], ['代文展', '2583753324@qq.com'],
         ['李波', '1341944815@qq.com'], ['罗明星', '1214916582@qq.com'], ['李永琪', '1214916582@qq.com'],
         ['蒋军尧', '1225447987@qq.com'], ['邱英雄', '13866675891@qq.com'], ['吴志明', '3524594569@qq.com'],
         ['黄栋高', '2641599176@qq.com'], ['刘烨', '1804573321@qq.com'], ['刘康伟', '774228636@qq.com'],
         ['徐帅', '2367058156@qq.com'], ['唐翔', '2230798802@qq.com'], ['周智', '2043673172@qq.com'],
         ['杨想响', '2670554361@qq.com'], ['王璞', '1714131532@qq.com'],
         ['曾杰', '2214550673@qq.com'], ['王鹏博', '2252656710@qq.com'], ['陈中闲', '2265741906@qq.com'],
         ['毛文韬', '2287025767@qq.com'], ['姜伟', '2469464856@qq.com'], ['王永强', '2849833803@qq.com'],
         ['王飞翔', '3110816003@qq.com'], ['王来宝', '1771756644@qq.com'], ['李正冬', '1994076371@qq.com'],
         ['黄瑞', '549532570@qq.com'], ['王博威', '3049649837@qq.com'], ['杨国锋', '1870775479@qq.com'],
         ['陈海豹', '2285038871@qq.com'], ['王峰', '1209302854@qq.com'], ['郭德地', '2966536366@qq.com'],
         ['李壮', '2689207093@qq.com'], ['马跃', '827002986@qq.com']]
    ClassHaveDone = []
    ClassNotDoneName = []
    ClassNotDoneEmail = []
    headers = {
        "Host": "dxx.ahyouth.org.cn",
        "Cookie": "PHPSESSID=662c565370b0dc460fdaae9ef0aa7004",
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_7 like Mac OS X) AppleWebKit/605.1.15 (KHTML, "
                      "like Gecko) Mobile/15E148 MicroMessenger/8.0.7(0x18000731) NetType/WIFI Language/zh_CN",
        "Accept-Language": "zh-cn",
        "Referer": "http://dxx.ahyouth.org.cn/",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive",
    }
    params = {
        "level1": "直属高校",
        "level2": "",
        "level3": "",
        "level4": "",
    }
    info = urlencode(params)
    tableName = GetNewTableName()
    URL = "http://dxx.ahyouth.org.cn/api/peopleRankStage?table_name=" + tableName + "&" + info
    info_rsp = requests.get(url=URL, headers=headers)
    info_json = info_rsp.json()
    AllInfoList = info_json['list']['list']
    for people in AllInfoList:
        ClassHaveDone.append(people['username'])
    for k in ClassAllListEmail:
        if k[0] not in ClassHaveDone:       # 如果这个同学没做的话
            ClassNotDoneEmail.append(k[1])   # 就添加Email在这其中
            ClassNotDoneName.append(k[0])   # 就添加Name在这其中
    for p in ClassNotDoneName:
        print("未完成同学：", p)
    return ClassNotDoneEmail


if __name__ == '__main__':
    # InitEmailInfo()
    GetNotFinishList()  # 拿到未完成名单但是不发邮件
    # Send_Email()      # 拿到未完成名单发送邮件
import re
import logging
import requests
from email.mime.text import MIMEText
import smtplib
from time import sleep
import pytesseract
from PIL import Image, ImageEnhance
from selenium import webdriver
from sqlalchemy import func
from model import User, db



def GetCookie(username, password):
    try:
        url = 'http://m.fjcyl.com/login'
        chrome_path = r"D:\Download\Dirver\chromedriver_win32\chromedriver_win32\chromedriver.exe"  # 驱动的路径
        # chrome_path = r".\web\chromedriver.exe"  # 驱动的路径
        driver = webdriver.Chrome(executable_path=chrome_path)
        driver.get(url)
        sleep(1)  # 等待网络

        driver.find_element_by_id('userName').clear()
        driver.find_element_by_id('userName').send_keys(username)

        driver.find_element_by_id('pwd').clear()
        driver.find_element_by_id('pwd').send_keys(password)

        driver.save_screenshot("./TempImage/01.png")  # 截取屏幕内容，保存到本地
        ran = Image.open("./TempImage/01.png")  # 打开截图，获取验证码位置，截取保存验证码
        box = (900, 690, 980, 750)  # 获取验证码位置,自动定位不是很明白，就使用了手动定位，代表（左，上，右，下）
        ran.crop(box).save("./TempImage/02.png")  # 把获取的验证码保存
        # 获取验证码图片，读取验证码
        imageCode = Image.open("./TempImage/02.png")  # 打开保存的验证码图片
        sharp_img = ImageEnhance.Contrast(imageCode).enhance(2.0)  # 图像增强，二值化
        sharp_img.save("./TempImage/03.png")  # 保存图像增强，二值化之后的验证码图片
        sharp_img.load()  # 对比度增强
        img = Image.open('./TempImage/03.png')
        img = img.convert('RGB')  # 这里也可以尝试使用L
        enhancer = ImageEnhance.Color(img)
        enhancer = enhancer.enhance(0)
        enhancer = ImageEnhance.Brightness(enhancer)
        enhancer = enhancer.enhance(2)
        enhancer = ImageEnhance.Contrast(enhancer)
        enhancer = enhancer.enhance(8)
        enhancer = ImageEnhance.Sharpness(enhancer)
        img = enhancer.enhance(20)
        code = pytesseract.image_to_string(img)
        # print(code)  # 输出验证码
        driver.find_element_by_id('VALIDATE_CODE').send_keys(code)
        element1 = driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/input")
        driver.execute_script("arguments[0].click();", element1)
        dictCookies = driver.get_cookies()  # 获取cookie
        sleep(2)
        driver.close()
        return dictCookies[0]["value"]
    except Exception as err:
        logging.error("开启浏览器 ERROR")
        return "500"


DidDone = []

session = requests.Session()
BASE_INFO = {
    "abbreviation": "",
    "orgId": "",
    "address": "",
    "orgName": "",
}


# 2团支书  3普通团员
def GetStuInfo(headers):  # 判断是团支书还是普通团员
    URL = "http://m.fjcyl.com/admin/user/getInfo?orgId={}".format(BASE_INFO["orgId"])
    BodyInfo = {}
    info_rsp = session.post(url=URL, headers=headers)
    info_json = info_rsp.json()
    print(info_json)
    positionName = info_json["rs"]["positionName"]
    acctId = info_json["rs"]["acctId"]
    orgName = info_json["rs"]["orgName"]
    UserName = info_json["rs"]["name"]  # 姓名
    gradeRe = re.findall('(\d+)', orgName)
    grade = gradeRe[0]  # 2019年级
    majorRe = re.findall('级(.+)团支部', orgName)
    major = majorRe[0]  # xxx专业
    collegeName = info_json["rs"]["cylMembers"]["orgName"]
    schoolNameRe = re.findall('共青团(.*)大学', collegeName)
    schoolName = schoolNameRe[0] + "大学"     # xx大学
    colNameRe = re.findall('大学(.*)委员会', collegeName)
    colName = colNameRe[0]                      # xxx学院
    BodyInfo["positionName"] = positionName
    BodyInfo["schoolName"] = schoolName
    BodyInfo["colName"] = colName
    BodyInfo["grade"] = grade
    BodyInfo["major"] = major
    BodyInfo["acctId"] = acctId
    BodyInfo["UserName"] = UserName
    count = db.session.query(func.count(User.id)).filter(User.school == schoolName, User.college == colName,
                                                         User.major == major, User.account == acctId).scalar()
    if count != 0:
        if positionName == "普通团员":
            return 3, BodyInfo, 10001  # 已经存在了
        elif positionName == "团支书":
            return 2, BodyInfo, 10001
    elif count == 0:
        if positionName == "普通团员":
            return 3, BodyInfo, 10002  # 未存在了
        elif positionName == "团支书":
            return 2, BodyInfo, 10002


def GetSchoolInfo(headers):  # 学校信息
    try:
        URL = "http://m.fjcyl.com/admin/user/orgList"
        info_rsp = session.post(url=URL, headers=headers)
        info_json = info_rsp.json()
        abbreviation = info_json["rs"][0]["cylorganization"]["abbreviation"]  # 19大数据
        orgId = info_json["rs"][0]["cylorganization"]["orgId"]  # 个人id
        address = info_json["rs"][0]["cylorganization"]["address"]  # 福州大学
        orgName = info_json["rs"][0]["cylorganization"]["orgName"]  # 福州大学数学与计算机科学学院2019级大数据团支部
        BASE_INFO["abbreviation"] = abbreviation
        BASE_INFO["orgId"] = orgId
        BASE_INFO["address"] = address
        BASE_INFO["orgName"] = orgName
        # print("BASE_INFO")
        # print(BASE_INFO)
        return "200"
    except Exception as err:
        print(err)
        return "500"


def LastestNum(headers):  # 获取最新一期的青年大学习的id
    URL = "http://m.fjcyl.com/admin/cylOrgMembers/groupByList?groupBy=1"
    info = URL
    info_rsp = session.post(url=info, headers=headers)
    info_json = info_rsp.json()
    x = info_json['rs'][0]['quarterNo']
    return x


def LastestURL(headers):  # 获取最新的链接，id是日期
    num = LastestNum(headers)
    URL = "http://m.fjcyl.com/admin/cylOrgMembers/selectList?orderBy=1&quarterNo={}".format(num)
    info = URL
    info_rsp = session.post(url=info, headers=headers)
    info_json = info_rsp.json()
    Ls = info_json["rs"]
    StudyTdLists = []
    for k in Ls:
        StudyTdLists.append(k['guoupStudyId'])
    return max(StudyTdLists)


def GetInfo(i,headers):  # 获取没做名单
    num = LastestURL(headers)
    URL = "http://m.fjcyl.com/admin/cylOrgMembers/selectCurrentStudy?studyId={}&" \
          "current=&PAGE_SIZE=20&CURRENT_PAGE={}&orgId={}".format(
        num, i, BASE_INFO["orgId"])
    info = URL
    info_rsp = session.post(url=info, headers=headers)
    info_json = info_rsp.json()
    List = info_json["rs"]['rs']
    # print(List)
    for detail in List:
        if detail['isStudy'] != '是':
        # if detail['isStudy'] == '是':
            DidDone.append(detail['acctName'])
    return DidDone


def Parma(headers):
    Temp1 = GetInfo(1, headers)
    Temp2 = GetInfo(2, headers)
    Temp3 = GetInfo(3, headers)
    Temp = Temp1 + Temp2 + Temp3
    DidDoneNumList = []
    for k in Temp:
        if k not in DidDoneNumList:
            DidDoneNumList.append(k)  # 将前面的列表集合化,因为有重复的
    if len(DidDoneNumList) == 0:
        # print("全部都完成了")
        return "0"
    DidDoneNumList_Json = []
    for name in DidDoneNumList:
        Num_Email = {}  # key是名字 value是邮箱
        try:        # 查询数据库中没有做的名单的邮箱地址
            DidNumEmail = User.query.filter_by(name=name).all()
            Num_Email["name"] = ("{}".format(name))             # 转成字符串
            Num_Email["email"] = ("{}".format(DidNumEmail[0]))  # 转成字符串
            DidDoneNumList_Json.append(Num_Email)
        except Exception as a:
            print("ERROR", a)
    strinfo = re.compile("'")
    Num_Email = str(DidDoneNumList_Json)
    Num_Email_Json = strinfo.sub('"', Num_Email)
    return Num_Email_Json


def Send_Email():
    msg = MIMEText('青年大学习！不用回复！赶紧做！！')  # 构造邮件，内容为青年大学习
    msg["Subject"] = "青年大学习！！又是你！！！"  # 设置邮件主题
    msg["From"] = '最劳累的团支书'  # 寄件者
    msg["To"] = '未做人员'  # 收件者
    from_addr = ''  # 邮箱
    password = ''   # 授权码
    smtp_server = 'smtp.qq.com'                 # smtp服务器地址
    to_addr = Parma()                           # 收件人地址
    print("to_addr")
    print(to_addr)
    try:
        # smtp协议的默认端口是25，QQ邮箱smtp服务器端口是465,第一个参数是smtp服务器地址，第二个参数是端口，第三个参数是超时设置,这里必须使用ssl证书，要不链接不上服务器
        server = smtplib.SMTP_SSL(smtp_server, 465, timeout=2)
        server.login(from_addr, password)  # 登录邮箱
        # 发送邮件，第一个参数是发送方地址，第二个参数是接收方列表，列表中可以有多个接收方地址，表示发送给多个邮箱，msg.as_string()将MIMEText对象转化成文本
        server.sendmail(from_addr, to_addr, msg.as_string())
        server.quit()
        print('success')
    except Exception as e:
        # Todo 记得做完要发送到2681272923@qq.com这个邮箱
        if e == None:
            # Send_Boss()
            print('Faild:%s' % e)
            pass


# 输出时间
def job():
    Send_Email()

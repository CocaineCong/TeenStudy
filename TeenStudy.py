import requests
from email.mime.text import MIMEText
import smtplib
from time import sleep
import pytesseract
from PIL import Image, ImageEnhance
from selenium import webdriver

username = input("请输入手机号:")
password = input("请输入密码:")

DidDone = []

session = requests.Session()
BASE_INFO = {
    "abbreviation": "",
    "orgId": "",
    "address": "",
    "orgName": "",
}

Email = [
    ['张三', '11111@qq.com'], ['李四', '22222@qq.com'],
    ['老王', '333333@qq.com'], ['小王', '444444@qq.com'],  # TODO 这里记得要改
]


def GetCookie(username, password):
    try:
        url = 'http://m.fjcyl.com/login'
        chrome_path = r"D:\Download\Dirver\chromedriver_win32\chromedriver.exe"  # 驱动的路径
        driver = webdriver.Chrome(executable_path=chrome_path)
        driver.get(url)
        # sleep(1)  # 等待网络

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
        print(code)  # 输出验证码
        driver.find_element_by_id('VALIDATE_CODE').send_keys(code)
        element1 = driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/input")
        driver.execute_script("arguments[0].click();", element1)
        dictCookies = driver.get_cookies()  # 获取cookie
        sleep(2)
        driver.close()
        return dictCookies[0]["value"]
    except Exception as err:
        return "500"

# 请求头
headers = {
    'Host': 'm.fjcyl.com',
    'Referer': 'http://m.fjcyl.com/',
    'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 13_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) '
                  'Mobile/15E148 MicroMessenger/7.0.12(0x17000c33) NetType/WIFI Language/zh_CN',
    'Cookie': 'JSESSIONID='+GetCookie(username, password)
}


def GetSchoolInfo():  # 学校信息
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
        return BASE_INFO
    except Exception as err:
        print(err)
        return "500"


def LastestNum():        # 获取最新一期的青年大学习的id
    URL = "http://m.fjcyl.com/admin/cylOrgMembers/groupByList?groupBy=1"
    info = URL
    info_rsp = session.post(url=info, headers=headers)
    info_json = info_rsp.json()
    x = info_json['rs'][0]['quarterNo']
    return x


def LastestURL():            # 获取最新的链接，id是日期
    num = LastestNum()
    URL = "http://m.fjcyl.com/admin/cylOrgMembers/selectList?orderBy=1&quarterNo={}".format(num)
    info = URL
    info_rsp = session.post(url=info, headers=headers)
    info_json = info_rsp.json()
    Ls = info_json["rs"]
    StudyTdLists = []
    for k in Ls:
        StudyTdLists.append(k['guoupStudyId'])
    return max(StudyTdLists)


def GetInfo(i):  # 获取没做名单
    num = LastestURL()
    URL = "http://m.fjcyl.com/admin/cylOrgMembers/selectCurrentStudy?studyId={}&" \
          "current=&PAGE_SIZE=20&CURRENT_PAGE={}&orgId={}".format(
        num, i, BASE_INFO["orgId"])
    info = URL
    info_rsp = session.post(url=info, headers=headers)
    info_json = info_rsp.json()
    List = info_json["rs"]['rs']
    # print(List)
    for detail in List:
        # if detail['isStudy'] == '是':
        if detail['isStudy'] != '是':
            DidDone.append(detail['acctName'])
    return DidDone


def Parma():    # 我们班有3页，所以就直接这样了
    Temp1 = GetInfo(1)
    Temp2 = GetInfo(2)
    Temp3 = GetInfo(3)
    Temp = Temp1 + Temp2 + Temp3   # 这里是将没有做的同学记录下来
    DidDoneEmail = []   # 这里是将没有做的同学记录下来
    if len(Temp) == 0:
        print("全部都完成了")
        return 0
    else:
        for k in Temp:
            print("未完成同学：" + k)
    for i in range(len(Email)):
        if Email[i][0] in Temp:
            DidDoneEmail.append(Email[i][1])
    return DidDoneEmail


def Send_Email():
    msg = MIMEText('青年大学习！不用回复！赶紧做！！')  # 构造邮件，内容为青年大学习
    msg["Subject"] = "青年大学习！！又是你！！！"  # 设置邮件主题
    msg["From"] = ''  # 寄件者
    msg["To"] = '未做人员'  # 收件者
    from_addr = ''              # TODO 这里记得写你的邮箱地址
    password = ''               # TODO 这里记得更改上面from_addr的邮箱的申请码
    smtp_server = 'smtp.qq.com'   # smtp服务器地址
    to_addr = Parma()  # 收件人地址
    try:
        # smtp协议的默认端口是25，QQ邮箱smtp服务器端口是465,第一个参数是smtp服务器地址，第二个参数是端口，第三个参数是超时设置,这里必须使用ssl证书，要不链接不上服务器
        server = smtplib.SMTP_SSL(smtp_server, 465, timeout=2)
        server.login(from_addr, password)  # 登录邮箱
        # 发送邮件，第一个参数是发送方地址，第二个参数是接收方列表，列表中可以有多个接收方地址，表示发送给多个邮箱，msg.as_string()将MIMEText对象转化成文本
        server.sendmail(from_addr, to_addr, msg.as_string())
        server.quit()
        print('success')
    except Exception as e:
        if e == None:
            # Send_Boss()
            print('Faild:%s' % e)
            pass


if __name__ == '__main__':
    GetSchoolInfo()
    Parma()

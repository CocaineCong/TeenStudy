# coding:utf-8
import json
import logging
import re
import smtplib
from email.mime.text import MIMEText

import xlrd
from flask import request, jsonify, render_template
from sqlalchemy import func
from model import app, db, User
from spider import GetCookie, Parma, GetSchoolInfo, GetStuInfo


@app.route('/test', methods=['GET', 'POST'])
def hello_world():
    results = {
        "msg": "200",
        "data": {
            "Finally": [
                "xxx",
                "xxxxx"
            ]
        },
        "numEmail": {
            "xxxxx": "xxxxxxx@qq.com",
            "xxxx": "wwwwwwwww"
        }
    }
    return results


@app.route('/login', methods=['GET', 'POST'])  # 注意传输数据的时候的加密机制！！！
def login():
    username = request.form.get("username")
    password = request.form.get("password")
    cookie = GetCookie(username, password)
    if cookie == "500":
        return {
            "code": "500",
            "msg": "发生了点错误,请稍后重试"
        }
    headers = {
        'Host': 'm.fjcyl.com',
        'Referer': 'http://m.fjcyl.com/logout',
        'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 13_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) '
                      'Mobile/15E148 MicroMessenger/7.0.12(0x17000c33) NetType/WIFI Language/zh_CN',
        'Cookie': 'JSESSIONID=' + cookie
    }
    GetSchoolInfo(headers)
    cate, infoDetail, reg = GetStuInfo(headers)
    if cate == 3:  # 普通团员
        if reg == 10001:
            return {
                "code": 200,
                "msg": 3,  # 普通团员
                "info": 10001,
                "infoDetail": infoDetail,
            }
        elif reg == 10002:
            return {
                "code": 200,
                "msg": 3,  # 普通团员
                "info": 10002,
            }
    elif cate == 2:  # 团支书
        DidNumListT = Parma(headers)
        # print("DidNumListT")
        # print(DidNumListT)
        if len(DidNumListT) == 0:
            return {
                "code": 200
            }
        if reg == 10001:
            result = {
                "code": "200",
                "info": 10001,  # 还没在数据库中存在
                "msg": 2,  # 团支书
                "data": eval(DidNumListT),
                "infoDetail": infoDetail,
            }
            return result
        elif reg == 10002:
            result = {
                "code": "200",
                "msg": 2,  # 团支书
                "info": 10002,  # 在数据库中不存在
                "data": eval(DidNumListT)
            }
            return result


@app.route('/init_email', methods=['GET', 'POST'])
def init_email():
    QQEmail = request.form.get("QQEmail")
    UserName = request.form.get("UserName")
    acctId = request.form.get("acctId")
    colName = request.form.get("colName")
    grade = request.form.get("grade")
    major = request.form.get("major")
    positionName = request.form.get("positionName")
    schoolName = request.form.get("schoolName")
    count = db.session.query(func.count(User.id)).filter(User.school == schoolName, User.college == colName,
                                                         User.major == major, User.account == acctId).scalar()
    if count == 0:
        user = User(account=acctId, name=UserName, school=schoolName, college=colName,
                    grade=grade, major=major, origirtion=positionName, email=QQEmail)
        db.session.add(user)
        db.session.commit()
        return {
            "msg": 200,
            "data": "success"
        }
    elif count != 0:
        return {
            "msg": 200,
            "data": 10001,  # 已经存在了
        }
#
# @admin.route("/admin/upload", methods=['POST'])
# @login_required("SuperAdmin")
# def upload():
#     file = request.files['file']
#
#     f = file.read()    # 文件内容
#     data = xlrd.open_workbook(file_contents=f)
#     table = data.sheets()[0]
#     names = data.sheet_names()  # 返回book中所有工作表的名字
#     status = data.sheet_loaded(names[0])  # 检查sheet1是否导入完毕
#     if status:
#         try:
#             for i in range(1, table.nrows):
#                 d = [cell.value for cell in table.row_slice(i)]
#                 user = User(
#                         workId=d[0],
#                         username=d[0],
#                         password=d[0],
#                         name=d[1],
#                         studentId=d[2],
#                         gender=d[3],
#                         building=d[4],
#                         room=d[5],
#                         grade=d[6],
#                         classNo=d[7],
#                         profession=d[8],
#                         campus=d[9],
#                         groupId=d[10],
#                         qq=d[11],
#                         phone=d[12],
#                         email=d[13]
#                     )
#                 db.session.add(user)
#                 user.rights.append(Right.query.filter_by(name="User").first())
#             db.session.commit()
#             return jsonify({'status': '200', "msg": "信息导入成功"})
#         except Exception as e:
#             db.session.rollback()
#             return jsonify({'status': '500', "msg": str(e)})
#     else:
#         return jsonify({'status': '500', "msg": "读取失败，请重试"})


@app.route('/initData')  # 增加流式文件上传
def initData():
    file = request.files['file']
    f = file.read()                     # 文件内容
    data = xlrd.open_workbook(file_contents=f)
    table = data.sheets()[0]
    names = data.sheet_names()  # 返回book中所有工作表的名字
    status = data.sheet_loaded(names[0])  # 检查sheet1是否导入完毕
    if status:
        try:
            for i in range(1, table.nrows):
                d = [cell.value for cell in table.row_slice(i)]
                user = User(
                    workId=d[0],
                    username=d[0],
                    password=d[0],
                    name=d[1],
                    studentId=d[2],
                    gender=d[3],
                    building=d[4],
                    room=d[5],
                    grade=d[6],
                    classNo=d[7],
                    profession=d[8],
                    campus=d[9],
                    groupId=d[10],
                    qq=d[11],
                    phone=d[12],
                    email=d[13]
                )
                db.session.add(user)
                user.append(User.query.filter_by(name="User").first())
            db.session.commit()
            return jsonify({'status': '200', "msg": "信息导入成功"})
        except Exception as e:
            db.session.rollback()
            return jsonify({'status': '500', "msg": str(e)})
    else:
        return jsonify({'status': '500', "msg": "读取失败，请重试"})


@app.route('/sendMail', methods=['GET', 'POST'])
def sendMail():
    # print("DidDoneLists")
    DidDoneLists = request.form.get("EmailList")
    DidDoneList = DidDoneLists.split(",")
    Email = []
    count = 1
    for k in DidDoneList:
        count += 1
        if count == 2:
            Email.append(k)
            count = 0
    print(Email)
    msg = MIMEText('青年大学习！不用回复！赶紧做！！')  # 构造邮件，内容为青年大学习
    msg["Subject"] = "青年大学习！！又是你！！！"   # 设置邮件主题
    msg["From"] = '辛苦勤劳艰苦奋斗的团支书'        # 寄件者
    msg["To"] = '未做人员'  # 收件者
    from_addr = ''  # 邮箱
    password = ''   # 密码
    smtp_server = 'smtp.qq.com'             # smtp服务器地址
    to_addr = Email  # 收件人地址
    try:
        # smtp协议的默认端口是25，QQ邮箱smtp服务器端口是465,第一个参数是smtp服务器地址，第二个参数是端口，第三个参数是超时设置,这里必须使用ssl证书，要不链接不上服务器
        server = smtplib.SMTP_SSL(smtp_server, 465, timeout=2)
        server.login(from_addr, password)  # 登录邮箱
        # 发送邮件，第一个参数是发送方地址，第二个参数是接收方列表，列表中可以有多个接收方地址，表示发送给多个邮箱，msg.as_string()将MIMEText对象转化成文本
        server.sendmail(from_addr, to_addr, msg.as_string())
        server.quit()
        logging.info("EMAIL SUCCESS")
        return {"code": "200", "info": "success"}
        # print('success')
    except Exception as e:
        if e is None:
            # Send_Boss()
            logging.error("EMAIL FAIL")
            return {"code": "200", "info": "success"}
        else:
            print('Faild:%s' % e)
            return {"code": "500", "info": "fail"}


@app.route('/', methods=['GET', 'POST'])  # 团支书登陆
def TZS():
    UserName = request.args.get("username")
    PassWord = request.args.get("password")
    return render_template("LBS/index.html")


@app.route('/admin/login', methods=['GET', 'POST'])  # 管理员登陆
def admin():
    return render_template("admin/index.html")


@app.route('/admin_test')
def admin_test():
    return render_template("LBS/main.html")


if __name__ == '__main__':
    app.run()

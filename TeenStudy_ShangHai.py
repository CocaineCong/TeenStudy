# -*- coding:utf-8 -*-
import os
import requests
import xlrd
from urllib.parse import urlencode

PATH = r"./class"

headers = {
    'Connection': 'keep-alive',
    'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Content-Type': 'application/json;charset=UTF-8',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua-mobile': '?0',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36',
    'sec-ch-ua-platform': '"Windows"',
    'Origin': 'https://qcsh.h5yunban.com',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Referer': 'https://qcsh.h5yunban.com/youth-learning/admin/login.php',
    'Accept-Language': 'zh-CN,zh;q=0.9',
}

data = '{"account":"","password":""}'


def GetAllClassPath(path):
    path_list = []
    for root, dirs, files in os.walk(path):
        for file in files:
            path_list.append(os.path.join(root, file))
    return path_list


def GetClassInfo(class_path):
    wb = xlrd.open_workbook(class_path)  # 打开excel
    sh = wb.sheet_by_name('Sheet1')  # 按工作簿定位工作表
    s = str.split(class_path, "\\")
    class_name = s[-1]
    listTemp = {}
    for i in range(1, sh.nrows):
        listTemp[int(sh.row_values(i)[1])] = sh.row_values(i)[2]
    return class_name, listTemp
    # print(class_name, listTemp)


def GetNid(accessToken):  # 获取这个学院的id
    params = (
        ('accessToken', accessToken),
    )
    resp = requests.get('https://qcsh.h5yunban.com/youth-learning/cgi-bin/branch-api/info',
                        headers=headers, params=params)
    info_json = resp.json()
    return info_json['result']['id']


def GetCourse(accessToken):  # 获取是哪一期的青年大学习
    params = (
        ('pageSize', '99'),
        ('pageNum', '1'),
        ('desc', 'startTime'),
        ('type', '\u7f51\u4e0a\u4e3b\u9898\u56e2\u8bfe'),  # 网上主题团课
        ('accessToken', accessToken),
    )
    resp = requests.get('https://qcsh.h5yunban.com/youth-learning/cgi-bin/branch-api/course/list',
                        headers=headers, params=params)
    info_json = resp.json()
    return info_json['result']['list'][0]['id']


def Spider(subOrg, all_name):
    finish_number = []
    session = requests.Session()
    resp = session.post('https://qcsh.h5yunban.com/youth-learning/cgi-bin/login', headers=headers, data=data)
    accessToken = resp.json()['result']['accessToken']
    nid = GetNid(accessToken)
    course = GetCourse(accessToken)
    # subOrg = subOrg.encode('unicode-escape').decode()
    params = (
        ('pageSize', '80'),
        ('pageNum', '1'),
        ('desc', 'createTime'),
        ('nid', nid),  # 学校id
        ('subOrg', subOrg),  # 班级id
        ('course', course),  # 哪一期的青年大学习
        ('accessToken', accessToken),
    )
    info_rsp = session.get('https://qcsh.h5yunban.com/youth-learning/cgi-bin/branch-api/course/records',
                           headers=headers, params=params)
    info_json = info_rsp.json()
    for k in info_json['result']['list']:
        finish_number.append(eval(k['cardNo']))
    if len(finish_number) == len(list(all_name.keys())):
        print("{}人全部完成了".format(len(finish_number)))
    else:
        for k in finish_number:
            try:
                if k not in list(all_name.keys()):
                    print("未完成名单：", all_name[k])
            except Exception as e:
                print("学号为{}的人，不在名单中".format(k))


def StartSpider(all_class_path):
    paths = GetAllClassPath(all_class_path)  # 拿到路径
    for path in paths:
        sub_org, all_name = GetClassInfo(path)
        tmp = str.split(sub_org, '.')
        Spider(tmp[0], all_name)


if __name__ == '__main__':
    StartSpider(PATH)  # 这个是存放的班级信息的花名册路径

import datetime
from bokeh.core.json_encoder import rd
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pymysql
from flask_cors import *
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
# from app import BASE_INFO

HOSTNAME = '127.0.0.1'
PORT = '3306'
DATABASE = 'teenstudy'
USERNAME = 'root'
PASSWORD = 'root'
db_url = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(
    USERNAME,
    PASSWORD,
    HOSTNAME,
    PORT,
    DATABASE,
)


class Config(object):
    SQLALCHEMY_DATABASE_URI = db_url
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True


app = Flask(__name__)
CORS(app, supports_credentials=True)
pymysql.install_as_MySQLdb()
app.config.from_object(Config)
db = SQLAlchemy(app)

manager = Manager(app)      # 数据迁移
Migrate(app, db)    # 第一个参数是flask实例，第二个参数SQLAlchemy实例
manager.add_command("db", MigrateCommand)

engin = create_engine(db_url)
Base = declarative_base(engin)
Session = sessionmaker(engin)
session = Session()

# Gen_Info_Rd = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
# rd = redis.Redis(host='localhost', port=6379, db=1, decode_responses=True)


# 用户模型
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    account = db.Column(db.String(18))  # 账号
    add_time = db.Column(db.DateTime, index=True, default=datetime.datetime.now())  # 创建时间
    email = db.Column(db.String(100))  # 邮箱
    name = db.Column(db.String(16))  # 名字
    province = db.Column(db.String(255))  # 省份
    school = db.Column(db.String(255))  # 学校
    college = db.Column(db.String(255))  # 学院
    origirtion = db.Column(db.String(255))  # 组织
    grade = db.Column(db.String(255))  # 年级
    major = db.Column(db.String(255))  # 专业
    count = db.Column(db.Boolean, default=False)  # 最新一期青年大学习是否有做
    history_count = db.Column(db.Integer, default=False)  # 本季青年大学习做了多少次
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), default=3)  # 管理身份

    # def __repr__(self):
    #     return """<users(id:%d,account:%s,add_time:%s,email:%s,name:%s,province:%s,school:%s,college:%s,grade:%s,
    #     count:%s,history_count:%d,role_id:%d)""" % (self.id, self.account, self.add_time,
    #            self.email, self.name, self.province,
    #            self.school, self.college, self.grade,
    #            self.count, self.history_count, self.role_id)

    def __repr__(self):
        return """%s""" % self.email

    # def to_dict(self):
    #     return {
    #         'username':self.name,
    #         'email':self.email
    #     }


# 身份模型
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(8), unique=True)  # 1、管理员， 2、团支书， 3、普通团员
    users = db.relationship('User', backref='role')

    def __repr__(self):
        return """
            <roles(id:%d,name:%s)
        """ % (self.id, self.name)


# 青年大学习模型
class TeenStudy(db.Model):
    __tablename__ = 'teenstudy'
    id = db.Column(db.Integer, primary_key=True)
    study_id = db.Column(db.String(255))  # 第几期，爬下日期
    study_title = db.Column(db.String(255))  # 这一期的名字
    add_time = db.Column(db.DateTime, index=True, default=datetime.datetime.now())

    def __repr__(self):
        return """<teenstudy(id:%d,study_id:%s,study_title:%s,
        add_time:%s)>""" % (self.id, self.study_id, self.study_title, self.add_time)


class admin(db.Model):      # 管理员
    __tablenaem__ = 'admin'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    password = db.Column(db.String(255))
    add_time = db.Column(db.DateTime, index=True, default=datetime.datetime.now())

    def __repr__(self):
        return """<teenstudy(id:%d,name:%s,password:%s,
            add_time:%s)>""" % (self.id, self.name, self.password, self.add_time)


def Find():
    num = User.query.filter_by(role_id=2).all()
    print(num[0])

#
# if __name__ == '__main__':
#     Find()

"""==========zhuming=========="""
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 用户id
    username = db.Column(db.String(20), unique=True, nullable=False)  # 用户名
    password = db.Column(db.String(255), nullable=False)  # 密码
    email = db.Column(db.String(50), unique=True)  # 邮箱
    is_delete = db.Column(db.Boolean, default=0)  # 账号状态（1已删除，0正常）
    regisdate = db.Column(db.DateTime, default=datetime.now)  # 注册账号时间

    __tablename__ = 'user'

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Article_type(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 文章分类id
    tp_name = db.Column(db.String(20), unique=True, nullable=False)  #  文章分类名
    arts = db.relationship('Article', backref='art_tp')  # 关联文章

    __tablename__ = 'article_type'

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 文章id
    title = db.Column(db.String(20), unique=True, nullable=False)  # 文章标题
    desc = db.Column(db.String(100), nullable=False)  # 文章简介
    content = db.Column(db.Text, nullable=False)  # 文章内容
    create_date = db.Column(db.DateTime, default=datetime.now)  # 文章创建时间
    tp_id = db.Column(db.Integer, db.ForeignKey('article_type.id'))  # 外键关联文章分类id

    __tablename__ = 'article'

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()




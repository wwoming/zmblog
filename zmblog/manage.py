"""==========zhuming=========="""


import redis
from flask import Flask
from flask_script import Manager
from flask_session import Session

from back.models import db
from back.views import back_blue
from web.views import web_blue

app = Flask(__name__)

# 第二步管理蓝图
app.register_blueprint(blueprint=back_blue, url_prefix='/back')
app.register_blueprint(blueprint=web_blue, url_prefix='/web')

manager = Manager(app)
# 配置session信息
app.secret_key = '123456'
app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_REDIS'] = redis.Redis(host='127.0.0.1', port=6379)
Session(app)

# 配置数据库连接信息，初始化app
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:zhuming@127.0.0.1:3306/zm_blog'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

if __name__ == '__main__':
    manager.run()

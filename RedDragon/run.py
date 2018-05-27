#coding=utf-8

from flask import Flask, url_for, request, redirect, render_template
from flask_bootstrap import Bootstrap
# bootstrap里包含有css、JavaScript、base.html等文件
from flask_moment import Moment
# 里面包含moment.js，Flask-Moment 还依赖于 jquery.js
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

import sys
#解决flash的一个bug
defaultencoding = 'utf-8'
if sys.getdefaultencoding() != defaultencoding:
    reload(sys)
    sys.setdefaultencoding(defaultencoding)


app = Flask(__name__)

#各项插件的配置
app.config['SECRET_KEY']='sruend'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost/sun?charset=utf8'#配置数据库
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
db = SQLAlchemy()
db.init_app(app)
bootstrap = Bootstrap(app)
moment=Moment(app)
login_manger=LoginManager()
login_manger.session_protection='strong'
login_manger.login_view='movie.login'
login_manger.init_app(app)
@login_manger.user_loader
def load_user(user_id):
    from models import Users
    return Users.query.get(int(user_id))


#蓝图注
def init():
    from views import movie
    app.register_blueprint(blueprint=movie,url_prefix='/movie')


if __name__ == '__main__':
    init()
    app.run(port=80,debug=True)
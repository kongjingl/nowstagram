# -*- encoding=UTF-8 -*-

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from flask_login import LoginManager


app = Flask(__name__)
app.jinja_env.add_extension('jinja2.ext.loopcontrols') #为了兼容break语句和continue语句
app.config.from_pyfile('app.conf')  #初始化app
db = SQLAlchemy(app)
app.secret_key='nowcoder'
login_manager = LoginManager(app)
login_manager.login_view = '/regloginpage/'

from nowstagram import views, models

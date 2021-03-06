# -*- encoding=UTF-8 -*-

from nowstagram import app, db, login_manager
from flask import render_template, redirect, request, flash, get_flashed_messages
from models import Image, User
import random, hashlib

from flask_login import login_user, logout_user, login_required

def redirect_with_msg(target, msg, category):
    if msg != None:
        flash(msg, category=category)
    return redirect(target)

@app.route('/')
def index():
    images = Image.query.order_by(db.desc(Image.id)).limit(10).all()
    return render_template('index.html', images = images)

@app.route('/image/<int:image_id>/')
def image(image_id):
    image = Image.query.get(image_id)
    if image == None:
        return redirect('/')
    return render_template('pageDetail.html', image = image)

@app.route('/profile/<int:user_id>/')
@login_required
def user(user_id):
    user = User.query.get(user_id)
    if user == None:
        return redirect('/')
    return render_template('profile.html', user = user)

@app.route('/regloginpage/',methods={'post','get'})
def regloginpage():
    msg=''
    for m in get_flashed_messages(with_categories=False, category_filter=['reglogin']):
        msg = msg + m
    # 如果已经登录的就跳到首页
    return render_template('/login.html', msg=msg, next=request.values.get('next'))

@app.route('/reg/', methods={'post','get'})
def reg():
    username = request.values.get('username').strip()
    password = request.values.get('password').strip()
    user = User.query.filter_by(username=username).first()
    if user ==''or password=='':
        return  redirect_with_msg('/regloginpage/',u'用户名和密码不能为空','reglogin')

    if user != None:
        return redirect_with_msg('/regloginpage/',u'用户名已存在','reglogin')

    salt = ''.join(random.sample('0123456789abcdefghLMNOPQRSTUVWXYZ', 10))
    m = hashlib.md5()
    m.update(password + salt)
    password = m.hexdigest()
    user = User(username, password, salt)
    db.session.add(user)
    db.session.commit()

    login_user(user)

    next = request.values.get('next')
    if next != None and next.startswith('/') > 0:
        return redirect(next)

    return redirect('/')

@app.route('/login/', methods={'get', 'post'})
def login():
    username = request.values.get('username').strip()
    password = request.values.get('password').strip()
    # 校验
    user = User.query.filter_by(username=username).first()
    if username == '' or password == '':
        return redirect_with_msg('/regloginpage', u'用户名和密码不能为空', 'reglogin')

    user = User.query.filter_by(username=username).first()
    if user == None:
        return redirect_with_msg('/regloginpage', u'用户名不存在', 'reglogin')

    m = hashlib.md5()
    m.update(password + user.salt)
    if m.hexdigest() != user.password:
        return redirect_with_msg('/regloginpage', u'密码错误', 'reglogin')

    login_user(user)

    next = request.values.get('next')
    if next != None and next.startswith('/') :
        return redirect(next)


    return redirect('/')

@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')













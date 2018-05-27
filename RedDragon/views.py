# coding=utf-8
from  flask import render_template, Blueprint, redirect, url_for, flash
from run import login_manger
from forms import Login_Form, Register_Form, Recommond_Form
from models import Users
from flask_login import LoginManager, login_user, UserMixin, logout_user, login_required
from run import db
from datetime import datetime
from recommend import guess
import random

movie = Blueprint('movie', __name__)  # 蓝图


@movie.route('/')
def index():
    form = Login_Form()
    return render_template('login.html', form=form)


@movie.route('/login', methods=['GET', 'POST'])
def login():
    form = Login_Form()
    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data).first()
        if user is not None and user.password == form.password.data:
            login_user(user)
            flash(u'登录成功')
            return render_template('text.html', username=form.username.data, current_time=datetime.utcnow())
        else:
            flash(u'用户或密码错误')
            return render_template('login.html', form=form)


# 用户登出
@movie.route('/logout')
@login_required
def logout():
    logout_user()
    flash(u'你已退出登录')
    return redirect(url_for('movie.index'))


@movie.route('/register', methods=['GET', 'POST'])
def register():
    form = Register_Form()
    if form.validate_on_submit():
        user_Inquire = Users.query.filter_by(username=form.username.data).first()
        if user_Inquire is None:
            user = Users(username=form.username.data, password=form.password.data)
            # suiji_num = str(random.randint(0,9))+str(random.randint(0,9))+str(random.randint(0,9))+str(random.randint(0,9))
            # email_send(form.email.data, suiji_num)
            # if form.num.data == suiji_num:
            db.session.add(user)
            db.session.commit()
            flash(u'注册成功')
            return redirect(url_for('movie.index'))
            # else:
            #  flash(u"验证码错误！再试一次？重新填写？")
            #  return render_template('register.html', form=form)
        else:
            flash(u"您已注册！需要登录？")
            return redirect(url_for('movie.index'))
    return render_template('register.html', form=form)


import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib


def email_send(to_user, num):
    msg = MIMEMultipart('mixed')
    msg['Subject'] = u'注册红龙需要您完成邮箱验证！'
    msg['From'] = u'红龙'
    msg['To'] = to_user
    msg['Data'] = time.ctime()
    text = u"欢迎加入红龙！验证码是：" + num
    text_plain = MIMEText(text, 'plain', 'utf-8')
    msg.attach(text_plain)
    smtp = smtplib.SMTP_SSL("smtp.qq.com", 465)
    smtp.set_debuglevel(1)
    smtp.login('2436437774@qq.com', 'rjzitqsxhqmyebid')
    smtp.sendmail('2436437774@qq.com', to_user, msg.as_string())
    smtp.quit()


@movie.route('/recommond', methods=['GET', 'POST'])
def recommond():
    form = Recommond_Form()
    movie_list = []
    movie_href_list = []
    movie_pic_list = []
    if form.validate_on_submit():
        id = form.id.data
        #print id,type(id)
        flash(u'开始运行！正在处理数据，这可能需要您等待若干秒......')

        result = guess.run_recommond(id)

        for item in result:
            movie_list.append(item[0])
            m_h,p_h=get_movie_pic_and_url(item[0])
            if m_h is None:
                m_h = 'no_href'
            if p_h is None:
                p_h = 'no_src'
            movie_href_list.append(m_h)
            movie_pic_list.append(p_h)
            print item[0]

    num_type = len(movie_list)
    num_type_half = int(num_type/2)
    return render_template('recommond.html', form=form, df=movie_list, df2=movie_href_list, df3 = movie_pic_list, num = num_type, num_half = num_type_half)


import requests
from lxml import etree
from urlparse import urljoin
def get_movie_pic_and_url(name):
    url = 'https://www.imdb.com/find?ref_=nv_sr_fn&q='+name
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'}
    search_html = requests.get(url, headers=headers).content
    search_html_x = etree.HTML(search_html)
    movie_href=urljoin(url, search_html_x.xpath('//table[@class="findList"]//a[1]/@href')[0])

    movie_html = requests.get(movie_href, headers=headers).content
    movie_html_x = etree.HTML(movie_html)
    pic_href = movie_html_x.xpath('//div[@class="poster"]//img/@src')[0]

    return movie_href, pic_href
from flask import render_template, redirect, request, url_for, flash, make_response, jsonify, session, current_app
from flask_login import login_user, login_required, current_user, logout_user
from . import auth
from ..models import User
from .forms import LoginForm, RegistrationForm, PasswordResetForm, UserInfomationForm, UploadImageForm, UpdateInfoForm
from .. import db, photos
from ..email import send_message
import os
from flask_datepicker import datepicker
from wtforms import Form
from app import constants, redis_store,CSRFProtect
import re
from sqlalchemy.exc import IntegrityError
from werkzeug import secure_filename
import json
from sqlalchemy import and_
@auth.route('/login',methods=['GET','POST'])
def login():
    """ 用戶登入
        參數 : 用戶名、密碼, json
    
    """
    
    """
    1. 獲取參數(在有前端情況下)
    req_dict = request.get_json()
    mobile = req_dict.get("mobile")
    password = req_dict("password")
    
    2. 校驗參數
    3. 參數完整的校驗
    if not all ([mobile,password]):
        return jsonify(error="錯誤",errmsg="參數不完整")
    
    4. 判斷手機號的格式
    if not re.match(r"1[34578]\d", mobile):
        return jsonify(error="參數錯誤",errmsg="手機格式不完整")
    """
    form=LoginForm()

    # 5. 判斷錯誤次數是否超過限制，如果超過限制，則返回
    #    redis紀錄: "access_num_請求的ip" : 次數
    user_ip = request.remote_addr #用戶的ip地址
    try:
        access_nums = redis_store.get("access_num_%s" % user_ip)
    except Exception as e:
        current_app.logger.error(e)
    else:
        if access_nums is not None and int(access_nums) >= constants.LOGIN_ERROR_MAX_TIMES:
            flash(u"請求次數頻繁，請稍後重試")
            return render_template('auth/login.html',form=form) 
            # return jsonify(error="請求錯誤", errmsg="錯誤次數過多，請稍後重試")

    # 6. 從數據庫中根據Email查詢用戶的數據對象
    try:
        user = User.query.filter_by(email=form.email.data).first()
    except Exception as e:
        current_app.logger.error(e)
        flash("獲取用戶信息失敗")
        # return jsonify(error="數據庫錯誤",errormsg="獲取用戶信息失敗")

    # 7. 用數據庫的密碼與用戶填寫的密碼進行對比驗證
    if form.validate_on_submit():
        if user is None or user.verify_password(form.password.data) is False:
        # 如果驗證失敗，記錄錯誤次數，返回信息
            try:
            # redis的ince可以對字符串類型的數字數據進行+1的操作，如果數據一開始不存在，則會初始化為1
                redis_store.incr("access_num_%s" % user_ip)
                redis_store.expire("access_num_%s" % user_ip, constants.LOGIN_ERROR_FORBID_TIME)
            except Exception as e:
                current_app.logger.error(e)
            flash(u"用戶名或密碼錯誤")
        # return jsonify(error="數據庫資料不存在",errmsg="用戶名或密碼錯誤")

        
    # 8. 如果驗證相同成功，保存登入狀態，在session中
        # session["name"] = user.username
        # session["cellphone"] = user.cellphone
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            session["cellphone"] = user.cellphone
            session["username"] = user.username
            flash(u"用戶登入成功")
            return redirect(request.args.get('next') or url_for('main.index'))
    return render_template('auth/login.html',form=form)    
        # return jsonify(error="登入成功",errormsg="登入成功")


# 前端獲取用戶登入狀態
@auth.route("/session",methods=["GET"])
def check_login():
    # 檢查登陸狀態
    # 嘗試從session中獲取用戶的名字
    name = session.get(username)
    # 如果session中數據name名字存在，則表示用戶已登錄，否則未登入
    if name is not None:
        flash (u"該用戶已登入")
    else:
        flash(u"該用戶未登入")



@auth.route('/logout')
@login_required
def logout():
    # 清除session數據
    session.clear()
    logout_user()
    flash('成功登出')
    return redirect(url_for('main.index'))

@auth.route('/register',methods=['GET','POST'])
def register():
    """註冊
    請求的參數 : 手機號、用戶名、密碼、身分證號碼、電子郵件
    參數格式 : json 
    """
    """
    # 獲取請求的json數據，返回字典
    req_dict = request.get_json()
    mobile = req_dict.get("mobile")
    password = req_dict.get("password")
    password2 = req_dict.get("password2")
    # 校驗參數
    if not all([mobile, password]):
        # 表示格式不對
        return jsonify(errno="參數錯誤",errmsg="參數不完整")
    if password != password2:
        return jsonify(error="參數錯誤", errmsg="密碼不完整")
    # 判斷手機號格式
    if not re.match(r"1[34578]\d{9}",mobile):
        # 表示格式不對
        return jsonify(error="參數錯誤",errmsg="手機號格式錯誤")
    
    # 從redis中取出短信驗證碼
    try:
        redis_store.get("sms_code_%s" % mobile)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno="數據庫異常"，errmsg="讀取真實短信驗證碼異常")
    # 判斷短信驗證碼是否過期
    if real_sms_cide is None:
        return jsonify(errno="沒有資料",errmsg="短信驗證碼失效")
    
    #刪除redis中的短信驗證法，防止重複使用校驗
    try:
        redis_store.delete("sms_code_%s"%mobile)
    except Exception as e:
        current_app.logger.error(e)
    # 判斷用戶填寫短信驗證碼的正確性
    if real_sms_code !=sms_code:
        return jsonify(errno="沒有資料",errmsg="短信驗證碼失效")
    

    # 判斷用戶的手機號是否註冊過
    ## try:
    ##     user = User.query.filter_by(mobile=mobile).first()
    ## except Exception as e:
    ##     current_app.logger.error(e)
    ##     return jsonify(errno="",errmsg="數據庫異常"):
    ## else:
    ##     if user is not None:
    ##         #表示手機號存在
    ##         return jsonify(errno="",errmsg="手機號存在")
    """
    form = RegistrationForm()
    # 保存用戶的註冊數據到數據庫中
    if form.validate_on_submit():
        user = User(username=form.username.data,
                email=form.email.data,
                cellphone=form.cellphone.data,
                password = form.password.data)
        try:
            db.session.add(user)
            db.session.commit()
            flash('註冊成功')
            return redirect(url_for('auth.login'))

        except Exception as e:
            db.session.rollback()
            current_app.logger.error(e)
            flash(u"查詢數據庫異常")
    # 保存登入狀態到session中
    session["name"] = form.username.data
    session["cellphone"] = form.cellphone.data
    return render_template('auth/registration.html',form=form)    

    
    

@auth.route('/information', methods=["POST","GET"])
@login_required
def information():
    """設置用戶頭像
    參數: 圖片(多媒體表單格式) 用戶id (g.user_id)
    """
    form = UserInfomationForm()

    if form.validate_on_submit():
        current_user.gender = form.gender.data
        current_user.birthday = form.birthday.data
        current_user.user_id = form.user_id.data
        current_user.country = form.country.data
        current_user.address = form.address.data
        current_user.LINE = form.LINE.data

        try:
            db.session.add(current_user)
            db.session.commit()
            flash('實名認證完成')
            return redirect(url_for('auth.my'))

        except Exception as e:
            db.session.rollback()
            current_app.logger.error(e)
            flash(u"查詢數據庫異常")
            
    return render_template("auth/information.html",form=form)


@auth.route("/images", methods=["POST","GET"])
@login_required
def save_images():
    form = UploadImageForm()
    if form.validate_on_submit():
        
        try:
            # 從from對象中保存圖片
            # photo = request.files("photo")
            # filename = photo.read()

            filename = photos.save(form.photo.data)
            filename ="images/"+ filename
            # 返回了文件的url路径，而不是文件路径
            file_url = photos.url(filename)
            current_user.image_url = filename

        except Exception as e:
            current_app.logger.error(e)
            flash(u"不支持該照片格式")
            return render_template('auth/images.html', form=form)        

        

        try:
            db.session.add(current_user)
            db.session.commit()
            flash(u'照片提交完成')
            return redirect(url_for("auth.my"))

        except Exception as e:
            db.session.rollback()
            current_app.logger.error(e)
            flash(u"查詢數據庫異常")

    return render_template('auth/images.html', form=form)
    
    





@auth.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.ping()



@auth.route('/password/reset')
def password_reset():
    return render_template("auth/password_reset.html")

@auth.route('/captcha/check',methods=["POST"])
def captcha_check():
    image_code = request.form.get("image_code")
    image_code_id = request.form.get("image_code_id")
    cellphone = request.form.get("cellphone")
    email = request.form.get("email")
    # 校驗參數
    if not all ([image_code_id,image_code]):
        return jsonify(errno=0,errmsg="參數不完整")
        # 從redis中取出真實的圖片驗證碼
    try:
        real_image_code = redis_store.get("image_code_%s"%image_code_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=0,errmsg="Redis數據庫錯誤")
    
    #判斷圖片驗證碼是否過期
    if real_image_code is None:
        #表示圖片驗證碼沒有或者過期
        return jsonify(errno=0,errmsg="圖片驗證碼失效")
    # 刪除redis中的圖片驗證碼，防止用戶使用同一個圖片驗證法驗證多次
    try:
        redis_store.delete("image_code_%s" %image_code_id)
    except Exception as e:
        current_user.logger.error(e)

    # 與用戶填寫的值進行對比
    if str(real_image_code).lower() != image_code.lower():
        # 表示用戶填寫錯誤
        return jsonify(errno=0,errmsg="數據錯誤")
    else:
        u = User.query.filter(and_(User.cellphone==cellphone, User.email==email)).first()
        if u is not None:
            return jsonify(errno=1,errmsg="數據查詢成功")
        else:
            return jsonify(errno=0,errmsg="數據查詢失敗")


@auth.route('/my')
def my():
    return render_template("my.html")


@auth.route('/info', methods=["POST","GET"])
@login_required
def update_info():
    form = UpdateInfoForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.cellphone = form.cellphone.data
        try:
            db.session.add(current_user)
            db.session.commit()
            flash(u'資料更新完成')
            return redirect(url_for('auth.my'))

        except Exception as e:
            db.session.rollback()
            current_app.logger.error(e)
            flash(u"填寫資料有誤")
    return render_template("auth/update_info.html", form=form)




























# @auth.route('/confirm/<token>')
# @login_required
# def confirm(token):
#     if current_user.confirmed:
#         return redirect(url_for('main.index'))
#     if current_user.confirm(token):
#         flash ('您的郵箱已經進行認證')
#     else:
#         flash('已經失效')
#     return redirect(url_for('main.index'))

# @auth.before_app_request
# def before_request():
#     if current_user.is_authenticated \
#         and not current_user.confirmed:
#         return redirect(url_for('auth.unconfirmed'))

# @auth.route('/unconfirmed')
# def unconfirmed():
#     if current_user.is_anonymous or current_user.confirmed:
#         return redirect(url_for('main.index'))
#     return redirect(url_for('auth/unconfirmed.html'))

# @auth.route('/confirm')
# @login_required
# def resend_confirmation():
#     token = current_user.generate_confirmation_token()
#     send_emil(current_user.email, '請確認您的帳戶', 'auth/email/confirm', user=current_user, token=token)
#     flash('已經發送確認郵件')
#     return redirect(url_for('main.index'))
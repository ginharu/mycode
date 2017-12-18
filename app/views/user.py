from flask import Blueprint, render_template, flash, redirect, url_for, request, current_app
from app.forms import RegisterForm, LoginForm, IconForm
from app.forms.user import PasswordForm, ResetForm, ChangeemailForm, ResetemailForm, RetrieveForm
from app.models import User
from app.extensions import db
from app.email import send_mail
from flask_login import login_user, logout_user, login_required, current_user
from app.extensions import photos
import os
from PIL import Image


user = Blueprint('user', __name__)


@user.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        # 创建User模型
        u = User(username=form.username.data, password=form.password.data, email=form.email.data)
        # 保存到数据库
        db.session.add(u)
        # 此时用户还没有添加到数据库中，因此没有id，无法生成token
        # 在这里需要手动提交，也就是立即将数据写入到数据库中
        db.session.commit()
        # 发送账户激活邮件
        token = u.generate_activate_token()
        send_mail(form.email.data, '账户激活', 'email/activate', token=token, username=u.username)
        flash('注册成功，激活邮件已发送至注册邮箱，请点击完成激活')
        return redirect(url_for('main.index'))
    return render_template('user/register.html', form=form)


@user.route('/activate/<token>')
def activate(token):
    if User.check_activate_token(token):
        flash('账户激活成功')
        return redirect(url_for('user.login'))
    else:
        flash('激活失败')
        return redirect(url_for('main.index'))

# 用户登录
@user.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        u = User.query.filter_by(username=form.username.data).first()
        if u is None:
            flash('无效的用户名')
        elif u.verify_password(form.password.data):
            # 用户登录，顺便可以完成'记住我'的功能
            login_user(u, remember=form.remember.data)
            # 若有目标地址，则跳转到该地址，没有则跳转到首页
            return redirect(request.args.get('next') or url_for('main.index'))
        else:
            flash('无效的密码')
    return render_template('user/login.html', form=form)


@user.route('/logout/')
# 保护路由
@login_required
def logout():
    # 退出当前登录的用户
    logout_user()
    flash('您已退出登录')
    return redirect(url_for('main.index'))


@user.route('/profile/')
def profile():
    return render_template('user/profile.html')

# 修改密码
@user.route('/revise',methods=['GET','POST'])
@login_required
def revise():
    form = PasswordForm()
    if form.validate_on_submit():
        u = User.query.filter_by(username=current_user.username).first()
        if u.verify_password(form.password.data):
            u.password = form.newpass.data
            db.session.add(u)
            db.session.commit()
            flash('密码修改成功,请重新登录')
            return redirect(url_for('user.logout'))
        else:
            flash('密码输入错误')
    return render_template('user/revise.html',form=form)

#找回密码
@user.route('/retrieve',methods=['GET','POST'])
def retrieve():
    form = RetrieveForm()
    if form.validate_on_submit():
        u=User.query.filter_by(username=form.username.data).first()
        if u is None:
            flash('用户名不存在')
        elif u.email == form.email.data:

            token = u.generate_activate_token()

            send_mail(form.email.data, '找回密码', 'email/retrieve', token=token, username=u.username)
            flash('邮件发送成功，请前往邮箱确认')
        else:
            flash('请输入正确的绑定邮箱')
    return  render_template('user/retrieve.html',form=form)

# 激活密码
@user.route('/retrieve/<token>',methods=['GET','POST'])
def find(token):
    form = ResetForm()
    if form.validate_on_submit():
        user =User.get_user_id(token)
        user.password = form.newpass.data
        db.session.add(user)
        db.session.commit()
        flash('密码修改成功！')
        return redirect(url_for('main.index'))

    return  render_template('user/reset.html',form=form)

# 修改邮箱
@user.route('/resetemail/',methods=['GET','POST'])
@login_required
def resetemail():
    user = current_user
    form = ResetemailForm()
    form.email.render_kw = {'value': user.email, 'readonly': 'readonly'}
    if form.validate_on_submit():
        u = User.query.filter_by(email=form.email.data).first()
        token = u.generate_activate_token()
        send_mail(form.email.data, '重置邮箱', 'email/resetemail', token=token, username=u.username)

        flash('邮件发送成功，请去旧邮箱激活')
    return render_template('user/resetemail.html',form=form)

#激活邮箱
@user.route('/changeemail/<token>',methods=['GET','POST'])
def changeemail(token):
    form = ChangeemailForm()
    if form.validate_on_submit():
        u=User.get_user_id(token)
        u.email = form.email.data
        db.session.add(u)
        db.session.commit()
        flash('邮箱修改成功')
        return  redirect(url_for('main.index'))
    return render_template('user/changeemail.html',form=form)



# 修改头像
@user.route('/change_icon/', methods=['GET', 'POST'])
def change_icon():
    form = IconForm()
    if form.validate_on_submit():
        # 获取上传文件的后缀
        suffix = os.path.splitext(form.icon.data.filename)[1]
        # 生成随机的文件名
        name = rand_str() + suffix
        photos.save(form.icon.data, name=name)
        # 生成固定大小的缩略图
        pathname = os.path.join(current_app.config['UPLOADED_PHOTOS_DEST'], name)
        # 打开文件
        img = Image.open(pathname)
        # 设置尺寸
        img.thumbnail((256, 256))
        # 保存缩略图
        img.save(pathname)
        # 删除原来的头像，default.jpg除外
        if current_user.icon != 'default.jpg':
            os.remove(os.path.join(current_app.config['UPLOADED_PHOTOS_DEST'], current_user.icon))
        # 保存到数据库中
        current_user.icon = name
        db.session.add(current_user)
        flash('头像已修改')
    return render_template('user/change_icon.html', form=form)


# 生成指定长度的随机字符串
def rand_str(length=32):
    import random
    base_str = 'abcdefghijklmnopqrstuvwxyz1234567890'
    return ''.join(random.choice(base_str) for i in range(length))

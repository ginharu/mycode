from flask import Blueprint, render_template, current_app, flash, redirect, url_for, request
from app.email import send_mail
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from app.forms import PostsForm,RelyForm
from flask_login import current_user
from app.models import Posts, Replys
from app.extensions import db


main = Blueprint('main', __name__)


@main.route('/', methods=['GET', 'POST'])
def index():
    # 发布博客
    form = PostsForm()
    repform = RelyForm()
    if form.submit1.data and form.validate():
        # 判断是否登录
        if current_user.is_authenticated:
            # 创建帖子对象
            user = current_user._get_current_object()
            p = Posts(content=form.content.data, user=user)
            # 保存到数据库
            db.session.add(p)
            return redirect(url_for('main.index'))
        else:
            flash('登录后才能发表')
            return redirect(url_for('user.login'))
    # 读取帖子
    #posts = Posts.query.filter_by(rid=0).order_by(Posts.timestamp.desc()).all()
    # 发表回复
    if repform.submit2.data and repform.validate():
        if current_user.is_authenticated:
            postid = repform.hidden.data
            user = current_user._get_current_object()
            r = Replys(content = form.content.data,user=user)
            post= Posts.query.filter_by(id=postid).first()
            r.posts.append(post)
            db.session.add(r)
            return redirect(url_for('main.index'))
        else:
            flash('登录后才能发表')
            return redirect(url_for('user.login'))
    # 读取分页数据
    # 获取页码
    page = request.args.get('page', 1, type=int)
    pagination = Posts.query.filter_by(rid=0).order_by(Posts.timestamp.desc()).paginate(page, per_page=5, error_out=False)
    posts = pagination.items

    replys = Replys.query.all()

    return render_template('main/index.html', form=form, posts=posts, pagination=pagination,repform=repform,replys=replys)

















@main.route('/mail/')
def send():
    send_mail('lizihao0913@163.com', '账户激活', 'email/activate', username='xiaoming')
    return '邮件已发送'


@main.route('/get_token/')
def generate():
    s = Serializer(current_app.config['SECRET_KEY'], expires_in=3600)
    return s.dumps({'id': 250})


@main.route('/activate/<token>')
def activate(token):
    s = Serializer(current_app.config['SECRET_KEY'])
    data = s.loads(token)
    return str(data.get('id'))

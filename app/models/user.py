from flask import current_app
from app.extensions import db
# 导入密码散列及校验函数
from werkzeug.security import generate_password_hash, check_password_hash
# 生成token使用的类
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from app.extensions import login_manager
# 用户状态的使用需要实现几个回调函数，UserMixin类已经做了实现
from flask_login import UserMixin


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(32), unique=True)
    confirmed = db.Column(db.Boolean, default=False)
    # 用户头像
    icon = db.Column(db.String(128), default='default.jpg')
    # 添加关联模型，动态添加一个字段
    posts = db.relationship('Posts', backref='user', lazy='dynamic')
    replys = db.relationship('Replys',backref = 'user',lazy = 'dynamic')

    # 保护字段
    @property
    def password(self):
        raise AttributeError('密码是不可读属性')

    # 设置密码（加密存储）
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    # 密码校验
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    # 生成账户激活的token
    def generate_activate_token(self, expires_in=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=expires_in)
        # 将字典数据进行串行化，生成带过期时间的乱码
        return s.dumps({'id': self.id})

    # 账户激活，因为激活时还不知道是哪个用户
    @staticmethod
    def check_activate_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        user = User.query.get(data.get('id'))
        if user is None:
            # 不存在此用户
            return False
        if not user.confirmed:
            # 若没有激活，则激活账户
            user.confirmed = True
            db.session.add(user)
        return True


# 登录认证的回调
@login_manager.user_loader
def loader_user(user_id):
    return User.query.get(int(user_id))

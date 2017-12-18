from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField,ValidationError
from wtforms.validators import DataRequired, Length, EqualTo, Email
from app.models import User
from app.extensions import photos


# 用户注册表单
class RegisterForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(), Length(2, 15, message='长度必须在2~15个字符之间')])
    password = PasswordField('密码', validators=[DataRequired(), Length(1, 18, message='长度必须在1~18个字符之间')])
    confirm = PasswordField('确认密码', validators=[EqualTo('password', message='两次密码不一致')])
    email = StringField('邮箱', validators=[Email(message='邮箱格式不正确')])
    submit = SubmitField('立即注册')

    # 自定义表单字段验证，书写 'validate_字段' 的函数，
    # 即可完成对应字段的自定义校验
    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('该用户已存在，请选用其它用户名')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('该邮箱已注册使用，请选用其它邮箱')


# 用户登录表单
class LoginForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired()])
    password = PasswordField('密码', validators=[DataRequired()])
    remember = BooleanField('记住我')
    submit = SubmitField('立即登录')


    def validate_username(self, field):
        if not User.query.filter_by(username=field.data).first():
            raise ValidationError('用户名不存在')

# 修改密码
class PasswordForm(FlaskForm):
    password = PasswordField('请输入旧密码', validators=[DataRequired()])
    newpass = PasswordField('请输入新密码', validators=[DataRequired(), Length(2, 10, message='密码长度在2-10位')])
    confirm = PasswordField('确认密码', validators=[EqualTo('newpass', '两次密码不一样')])
    submit = SubmitField('确认修改')

# 找回密码
class RetrieveForm(FlaskForm):
    username = StringField('请输入要找回密码的账号', validators=[DataRequired()])
    email = StringField('请输入该账号绑定的邮箱', validators=[Email(message='邮箱格式不正确')])
    submit = SubmitField('提交!')

# 重置密码
class ResetForm(FlaskForm):
    newpass = PasswordField('请输入新密码', validators=[DataRequired(), Length(2, 10, message='密码长度在2-10位')])
    confirm = PasswordField('确认密码', validators=[EqualTo('newpass', '两次密码不一样')])
    submit = SubmitField('确认修改')

# 修改邮箱
class ResetemailForm(FlaskForm):
    email = StringField('旧邮箱', validators=[Email(message='邮箱格式不正确')])
    newemail = StringField('请输入新邮箱', validators=[Email(message='邮箱格式不正确')])
    submit = SubmitField('发送验证信息')

class ChangeemailForm(FlaskForm):
    email = StringField('请输入新邮箱', validators=[Email(message='邮箱格式不正确')])
    submit = SubmitField('确认修改')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('该邮箱已被注册过，请选其他邮箱')


# 头像上传表单
class IconForm(FlaskForm):
    icon = FileField('头像', validators=[FileRequired('请选择文件'), FileAllowed(photos, '只能上传图片')])
    submit = SubmitField('立即上传')

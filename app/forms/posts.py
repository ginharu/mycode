from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, HiddenField
from wtforms.validators import DataRequired, Length


# 发表帖子的表单
class PostsForm(FlaskForm):
    content = TextAreaField('', render_kw={'placeholder': '这一刻得的想法...'}, validators=[DataRequired(), Length(5, 128, message='只能在5~128个字符之间')])
    submit1 = SubmitField('发表')

class RelyForm(FlaskForm):
    hidden = HiddenField('', render_kw={'value': ''}, validators=[DataRequired()])
    content = TextAreaField('', render_kw={'placeholder': '请输入回复内容'}, validators=[DataRequired()])
    submit2 = SubmitField('回复')
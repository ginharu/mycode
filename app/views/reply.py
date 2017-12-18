import random

from  flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import current_user

from app.extensions import db
from app.forms import PostsForm, RelyForm
from  app.models import Posts,User,Replys

reply = Blueprint('reply',__name__)

@reply.route('/index/<int:id>')
def postdel(id):
    posts = Posts.query.filter_by(id=id).first()
    for reply in posts.replys:
        repid = reply.id
        reply_del = Replys.query.filter_by(id=repid).first()
        db.session.delete(reply_del)
    db.session.delete(posts)
    db.session.commit()

    return redirect(url_for('main.index'))


@reply.route('/del/<int:id>')
def repdel(id):
    reply_del = Replys.query.filter_by(id=id).first()
    print(reply_del)
    db.session.delete(reply_del)
    db.session.commit()
    return redirect(url_for('main.index'))

# @reply.route('/reply/',methods = ['GET','POST'])
# def repajax():
#     form = PostsForm()
#     repform = RelyForm()
#     content = request.form.get('content','')
#     print(content)
#
#     if current_user.is_authenticated:
#         postid = id
#         user = current_user._get_current_object()
#         r = Replys(content = content,user=user)
#         post= Posts.query.filter_by(id=postid).first()
#         print(r,post)
#         r.posts.append(post)
#         db.session.add(r)
#         return redirect(url_for('main.index'))
#         # return str(content)
#     else:
#         flash('登录后才能发表')
#         return redirect(url_for('user.login'))

    # a = random.randint(1,10)
    # print(id,'%d'%a)




from app.extensions import db
from datetime import datetime

post_reply = db.Table(
    'post_reply',
    db.Column('posts_id',db.Integer,db.ForeignKey('posts.id')),
    db.Column('replys_id',db.Integer,db.ForeignKey('replys.id')),
)


class Posts(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    rid = db.Column(db.Integer, index=True, default=0)
    content = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    # 添加关联外键
    uid = db.Column(db.Integer, db.ForeignKey('users.id'))

    replys = db.relationship(
        'Replys',
        secondary = post_reply,
        backref = 'posts',
    )



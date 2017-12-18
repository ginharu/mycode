from datetime import datetime

from app.extensions import db


class Replys(db.Model):
    __tablename__ = 'replys'
    id = db.Column(db.Integer,primary_key=True)
    content = db.Column(db.Text)
    timestamp = db.Column(db.DateTime,default=datetime.utcnow)
    uid = db.Column(db.Integer,db.ForeignKey('users.id'))
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sport = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    location = db.Column(db.String(10000))
    creater_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    participant_number = db.Column(db.Integer)
    description = db.Column(db.String(10000))
    max_participants = db.Column(db.Integer)

class PostParticipant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    participant_id = db.Column(db.Integer, db.ForeignKey('user.id'))



class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))

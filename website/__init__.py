from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from apscheduler.schedulers.background import BackgroundScheduler

from datetime import datetime, timedelta

db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'xilinw'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    
    return app

'''
from website.email import send_email
from .models import User
from .models import Post
from .models import PostParticipant

def email_job():
    posts = Post.query.all()
    now = datetime.now()
    for post in posts:
        if now+timedelta(hours=24) >= post.date:
            print('testing where am i')
            participants = PostParticipant.query.filter_by(post_id=post.id).all()
            plist = []
            for p in participants:
                user = User.query.filter_by(id=p.participant_id).first()
                plist.append(user.email)

            subject = "Upgrade Reminder"
            message = 'Non-reply:\n This is just a friendly reminder that you registered ' + post.sport + ' game at ' + post.location + ' will happen in 24 hours!'
            print(message)
            # send_email(plist,subject,message)
    
    print('I am working...')

scheduler = BackgroundScheduler()
job = scheduler.add_job(email_job, 'interval', seconds=3)
scheduler.start()
'''

def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')
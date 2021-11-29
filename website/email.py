import smtplib

from datetime import datetime, timedelta
from .models import Post
from .models import PostParticipant
from .models import User


def send_email(recipient, subject, body):
    print("sending email")
    user = 'upgradematchweb@gmail.com'
    pwd = 'Aa12345678@'
    FROM = user
    TO = recipient if isinstance(recipient, list) else [recipient]
    SUBJECT = subject
    TEXT = body

    # Prepare actual message
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(user, pwd)
        server.sendmail(FROM, TO, message)
        server.close()
        print ('successfully sent the mail')
    except:
        print ("failed to send mail")

def email_job():
    posts = Post.query.all()
    now = datetime.now()
    for post in posts:
        if now+timedelta(hours=24) >= post.date:
            participants = PostParticipant.query.filter_by(post_id=post.id).all()
            plist = []
            for p in participants:
                user = User.query.filter_by(id=p.participant_id).first()
                plist.append(user.email)

            subject = "Upgrade Reminder"
            message = 'Non-reply:\n This is just a friendly reminder that you registered ' + post.sport + ' game at ' + post.location + ' will happen in 24 hours!'
            send_email(plist,subject,message)
    
    

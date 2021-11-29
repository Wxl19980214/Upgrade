from . import db
from .models import Post
from .models import PostParticipant
from .models import User
import smtplib
from datetime import datetime


now = datetime.now()

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
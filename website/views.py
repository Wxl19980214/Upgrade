from operator import pos
from flask import Blueprint, render_template, request, flash, jsonify
from flask.scaffold import _matching_loader_thinks_module_is_package
from flask_login import login_required, current_user

from website.email import send_email
from .models import Post
from .models import PostParticipant
from datetime import datetime
from . import db
import json

views = Blueprint('views', __name__)


@views.route('/home', methods=['GET'])
def home():
    return render_template("home.html", user=current_user)


@views.route('/view', methods=['GET', 'POST'])
def view():
    posts = Post.query.all()
    if request.method == 'POST':
        user_id = request.form.get('user_id')
        post_id = request.form.get('post_id')

        # if user already sign up in this post
        pps = PostParticipant.query.filter_by(post_id=post_id).all()
        for pp in pps:
            if str(pp.participant_id) == user_id:
                flash('You already signed up for this event', category='error')
                return render_template("view.html", user=current_user, all_post=posts)

        
    
        post = Post.query.filter_by(id=post_id).first()
        if post.max_participants > post.participant_number:
            new_pp = PostParticipant(post_id=post_id, participant_id=user_id)
            db.session.add(new_pp)
            db.session.commit()
            flash('Sign up successful', category='success')
            db.session.query(Post).filter(Post.id == post_id).update(
                {Post.participant_number: Post.participant_number + 1})
            db.session.commit()

            event = db.session.query(Post).filter(Post.id == post_id).first()
            sport = event.sport
            location = event.location
            date = event.date
            subject = sport + ' Event Post!'
            message = 'Non-reply: \nYou have successfully registered a ' + sport + ' game at ' + location + ' on ' + date.strftime("%m/%d/%Y, %H:%M:%S")
            send_email(current_user.email,subject, message)
        else:
            flash("This event is full! Check back later!", category='error')

    return render_template("view.html", user=current_user, all_post=posts)


@views.route('/plan', methods=['GET', 'POST'])
@login_required
def plan_event():
    if request.method == 'POST':
        sport = request.form.get('sport')
        html_date = request.form.get('date')
        location = request.form.get('location')
        post_description = request.form.get('description')
        max_participants = request.form.get('max_participants')
        if not sport:
            flash('You must enter a sport!', category='error')
            return render_template("plan.html", user=current_user)
        if not location:
            flash('You must enter a location!', category='error')
            return render_template("plan.html", user=current_user)
        if html_date:
            date = datetime.strptime(html_date, '%Y-%m-%dT%H:%M')
        else:
            flash('You must enter a time!', category='error')
            return render_template("plan.html", user=current_user)

        now = datetime.now()
        if date <= now:
            flash('Event must be in the future!', category='error')
            return render_template("plan.html", user=current_user)

        new_post = Post(sport=sport, date=date, location=location, creater_id=current_user.id, participant_number=1,
                        description=post_description, max_participants=max_participants)
        db.session.add(new_post)
        db.session.commit()

        # adding to PostParticipant
        post_id = Post.query.filter_by(sport=sport, date=date, location=location, creater_id=current_user.id).first().id
        new_pp = PostParticipant(post_id=post_id, participant_id=current_user.id)
        db.session.add(new_pp)
        db.session.commit()
        flash('Event Posted!', category='success')
        # sending email
        subject = sport + ' Event Post!'
        message = 'Non-reply: \nYou have successfully scheduled a ' + sport + ' game at ' + location + ' on ' + date.strftime("%m/%d/%Y, %H:%M:%S")
        send_email(current_user.email,subject, message)

    return render_template("plan.html", user=current_user)

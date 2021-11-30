from flask import Blueprint, render_template, request, flash, jsonify
from flask.scaffold import _matching_loader_thinks_module_is_package
from flask_login import login_required, current_user
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
@login_required
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

        if Post.max_participants == Post.participant_number:
            new_pp = PostParticipant(post_id=post_id, participant_id=user_id)
            db.session.add(new_pp)
            db.session.commit()
            flash('Sign up successful', category='success')
            db.session.query(Post).filter(Post.id == post_id).update(
                {Post.participant_number: Post.participant_number + 1})
            db.session.commit()
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
        date = datetime.strptime(html_date, '%Y-%m-%dT%H:%M')
        post_description = request.form.get('description')
        max_participants = request.form.get('max_participants')

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

    return render_template("plan.html", user=current_user)


@views.route('/post/<int:id>', methods=['POST','GET'])
def edit(id):
    post_to_edit = Post.query.get_or_404(id)
    if request.method == 'POST':
        post_to_edit.sport = request.form.get('sport')
        post_to_edit.max_participants = request.form.get('max_participants')
        post_to_edit.location = request.form.get('location')
        post_to_edit.description = request.form.get('description')
        date_edit = request.form.get('date')
        post_to_edit.date = datetime.strptime(date_edit, '%Y-%m-%dT%H:%M')
        try:
            db.session.commit()
            flash('Post edited!', category='success')

            return render_template("view.html", user=current_user,all_post=Post.query.all())
        except:
            return "Something happens when update this post..."
    else:
        return render_template('post.html', post_to_edit=post_to_edit, user=current_user)
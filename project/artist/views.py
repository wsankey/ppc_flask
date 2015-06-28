# project/artist/views.py


#################
#### imports ####
#################

import datetime

from flask import render_template, Blueprint, url_for, \
    redirect, flash, request
from flask.ext.login import login_user, logout_user, \
    login_required, current_user

from project.models import Artist
from project import db, bcrypt
from .forms import LoginForm, RegisterForm, ChangePasswordForm


################
#### config ####
################

artist_blueprint = Blueprint('artist', __name__,)


################
#### routes ####
################

@artist_blueprint.route('/artist/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if form.validate_on_submit():
        artist = Artist(
            email=form.email.data,
            password=form.password.data,
            confirmed=False
        )
        db.session.add(artist)
        db.session.commit()

        login_user(artist)

    return render_template('artist/register.html', form=form)


@artist_blueprint.route('/artist/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        artist = Artist.query.filter_by(email=form.email.data).first()
        if artist and bcrypt.check_password_hash(
                artist.password, request.form['password']):
            login_user(artist)
            flash('Welcome.', 'success')
            return redirect(url_for('main.home'))
        else:
            flash('Invalid email and/or password.', 'danger')
            return render_template('artist/login.html', form=form)
    return render_template('artist/login.html', form=form)


@artist_blueprint.route('/logout')
@login_required
def logout():
    logout_artist()
    flash('You were logged out.', 'success')
    return redirect(url_for('artist.login'))


@artist_blueprint.route('/artist/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = ChangePasswordForm(request.form)
    if form.validate_on_submit():
        artist = artist.query.filter_by(email=current_artist.email).first()
        if artist:
            artist.password = bcrypt.generate_password_hash(form.password.data)
            db.session.commit()
            flash('Password successfully changed.', 'success')
            return redirect(url_for('artist.profile'))
        else:
            flash('Password change was unsuccessful.', 'danger')
            return redirect(url_for('artist.profile'))
    return render_template('artist/profile.html', form=form)


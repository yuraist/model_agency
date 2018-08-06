from flask import render_template, url_for, redirect, flash
from flask_login import current_user, login_user, logout_user
from . import auth
from .forms import LoginForm, RegistrationForm
from app.models import User
from app import db


@auth.route('/register', methods=['get', 'post'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User()
        user.username = username
        user.password = password
        db.session.add(user)
        db.session.commit()
        flash('You are now a registered user')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)


@auth.route('/login', methods=['get', 'post'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = LoginForm()
    if form.validate_on_submit():
        # Get user data and user instance for the data
        username = form.username.data
        password = form.password.data
        remember_me = form.remember_me.data
        user = User.query.filter_by(username=username).first()

        # Verify username and password
        if user is None or not user.verify_password(password):
            flash('Invalid username or password')
            return redirect(url_for('.login'))
        login_user(user, remember=remember_me)
        return redirect(url_for('main.index'))
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))

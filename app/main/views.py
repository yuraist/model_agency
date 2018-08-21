import os

from flask import render_template, redirect, url_for, request, flash
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename

from . import main
from .forms import AddManagerForm, AddClubForm

from app import db
from app.models import User, Club, Model, Photo
from config import allowed_file, UPLOAD_FOLDER

from datetime import datetime


@main.route('/')
@login_required
def index():
    managers = User.query.all()
    models = Model.query.all()
    clubs = Club.query.all()
    return render_template('main.html', managers=managers,
                           models=models,
                           clubs=clubs)


@main.route('/register_manager', methods=['get', 'post'])
@login_required
def register_manager():
    form = AddManagerForm()
    if form.validate_on_submit():
        # Get the form data
        name = form.name.data
        username = form.username.data
        password = form.password.data

        # TODO: - Add uploading photo
        # Try to find an existing manager
        manager = User.query.filter_by(username=username).first()
        # If there is no manager with the username then create a new one
        if manager is None:
            # Create a new manager
            manager = User()
            manager.name = name
            manager.username = username
            manager.password = password

            # Save him into the database
            db.session.add(manager)
            db.session.commit()

        return redirect(url_for('main.manager', id=manager.id))
    return render_template('register_manager.html', form=form)


@main.route('/create_model', methods=['get', 'post'])
@login_required
def create_model():
    errors = []
    clubs = Club.query.all()

    if request.method == 'POST':
        model = Model()
        model.full_name = request.form['fullname']
        model.city = request.form['city']
        model.date_of_birth = datetime.strptime(request.form['date_of_birth'], '%d.%m.%Y').date()
        model.phone = request.form['phone']
        model.start_date = datetime.strptime(request.form['start_date'], '%d.%m.%Y').date()
        model.departure_date = datetime.strptime(request.form['departure_date'], '%d.%m.%Y').date()
        model.ticket_price = int(request.form['ticket_price'])
        model.club_id = int(request.form['club'])
        model.manager_id = current_user.id

        # Handle image uploading
        if 'file' in request.files:
            file = request.files['file']

            if file.filename == '':
                flash('Не выбран файл')
                return redirect(request.url)

            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(UPLOAD_FOLDER, filename)
                file.save(filepath)

                photo = Photo()
                photo.name = filename
                photo.url = filepath

                db.session.add(photo)
                db.session.commit()

                model.avatar_id = photo.id

        db.session.add(model)
        db.session.commit()

        return redirect(url_for('main.model', id=model.id))
    return render_template('create_model.html', clubs=clubs, errors=errors)


@main.route('/create_club', methods=['get', 'post'])
@login_required
def create_club():
    errors = []
    form = AddClubForm()
    if form.validate_on_submit():
        name = form.name.data
        city = form.city.data
        club = Club.query.filter_by(name=name).first()
        if club is not None:
            errors.append('Клуб уже есть в базе')
            return render_template('create_club.html', form=form, errors=errors)
        club = Club()
        club.name = name
        club.city = city

        db.session.add(club)
        db.session.commit()
        return redirect(url_for('main.club', id=club.id))

    return render_template('create_club.html', errors=errors, form=form)


@main.route('/manager/<id>')
def manager(id):
    manager = User.query.filter_by(id=id).first()
    models = manager.models
    return render_template('manager.html', manager=manager, models=models)


@main.route('/model/<id>')
def model(id):
    model = Model.query.filter_by(id=id).first()
    avatar = Photo.query.filter_by(id=model.avatar_id).first()
    return render_template('model.html', model=model, avatar_filename=avatar.name)


@main.route('/club/<id>')
def club(id):
    club = Club.query.filter_by(id=id).first()
    return render_template('club.html', club=club)

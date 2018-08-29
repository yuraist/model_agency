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
    managers = []
    models = []
    clubs = []
    if current_user.is_root:
        managers = User.query.order_by(User.id.desc()).all()
        models = Model.query.order_by(Model.id.desc()).all().copy()
        clubs = Club.query.order_by(Club.id.desc()).all()
    elif current_user.is_admin:
        models = Model.query.order_by(Model.id.desc()).all().copy()
    else:
        models = Model.query.filter_by(manager_id=current_user.id).order_by(Model.id.desc()).all().copy()

    for model in models:
        if model.end_date == "В архиве":
            models.remove(model)

    return render_template('main.html', managers=managers,
                           models=models,
                           clubs=clubs,
                           Photo=Photo)


@main.route('/register_manager', methods=['get', 'post'])
@login_required
def register_manager():
    form = AddManagerForm()
    if form.validate_on_submit():
        # Get the form data
        name = form.name.data
        username = form.username.data
        password = form.password.data
        is_admin = bool(form.is_admin.data)

        # Try to find an existing manager
        manager = User.query.filter_by(username=username).first()
        # If there is no manager with the username then create a new one
        if manager is None:
            # Create a new manager
            manager = User()
            manager.name = name
            manager.username = username
            manager.password = password
            manager.is_admin = is_admin

            # Handle image uploading
            file = form.photo.data
            if file is not None:
                if type(file) != str:
                    if file.filename == '':
                        flash('Не выбран файл')
                        return redirect(request.url)

                    if file and allowed_file(file.filename):
                        filename = secure_filename(file.filename)
                        file_path = os.path.join(UPLOAD_FOLDER, filename)
                        file.save(file_path)

                        photo = Photo()
                        photo.name = filename
                        photo.url = file_path

                        db.session.add(photo)
                        db.session.commit()

                        manager.avatar_id = photo.id

            # Save him into the database
            db.session.add(manager)
            db.session.commit()

        return redirect(url_for('main.manager', id=manager.id))
    return render_template('register_manager.html', form=form)


@main.route('/edit_manager/<id>', methods=['get', 'post'])
def edit_manager(id):
    manager = User.query.filter_by(id=id).first()
    if request.method == 'POST':
        name = request.form['name']
        username = request.form['username']
        password = request.form['password']
        is_admin = request.form.get('is_admin')
        print(is_admin)

        if name != None and name != '':
            manager.name = name

        if username != None and username != '':
            manager.username = username

        if is_admin != '':
            manager.is_admin = bool(is_admin)

        if password != None and password != '':
            manager.password = password

        db.session.add(manager)
        db.session.commit()
        return redirect(url_for('main.manager', id=manager.id))

    return render_template('edit_manager.html', manager=manager)


@main.route('/delete_manager/<id>')
def delete_manager(id):
    manager = User.query.filter_by(id=id).first()
    db.session.delete(manager)
    db.session.commit()
    return redirect(url_for('main.index'))


@main.route('/create_model', methods=['get', 'post'])
@login_required
def create_model():
    errors = []
    clubs = Club.query.all()

    if request.method == 'POST':
        model = Model()

        # Required fields
        model.full_name = request.form['fullname']
        model.city = request.form['city']
        model.date_of_birth = datetime.strptime(request.form['date_of_birth'], '%d.%m.%Y').date()

        # Optional fields
        model.phone = request.form['phone']
        if request.form['start_date'] != '':
            model.start_date = datetime.strptime(request.form['start_date'], '%d.%m.%Y').date()
        if request.form['period'] != '':
            model.period = int(request.form['period'])
        if request.form['departure_date'] != '':
            model.departure_date = datetime.strptime(request.form['departure_date'], '%d.%m.%Y').date()

        if request.form['ticket_price'] != '':
            model.ticket_price = float(request.form['ticket_price'])
        if request.form['club'] != '':
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
                file_path = os.path.join(UPLOAD_FOLDER, filename)
                file.save(file_path)

                photo = Photo()
                photo.name = filename
                photo.url = file_path

                db.session.add(photo)
                db.session.commit()

                model.avatar_id = photo.id

        db.session.add(model)
        db.session.commit()

        return redirect(url_for('main.model', id=model.id))
    return render_template('create_model.html', clubs=clubs, errors=errors)


@main.route('/edit_model/<id>', methods=['get', 'post'])
def edit_model(id):
    if request.method == 'GET':
        model = Model.query.filter_by(id=id).first()
        clubs = Club.query.all()
    elif request.method == 'POST':
        model = Model.query.filter_by(id=id).first()
        # Required fields
        model.full_name = request.form['fullname']
        model.city = request.form['city']
        model.date_of_birth = datetime.strptime(request.form['date_of_birth'], '%d.%m.%Y').date()

        # Optional fields
        model.phone = request.form['phone']
        if request.form['start_date'] != '':
            model.start_date = datetime.strptime(request.form['start_date'], '%d.%m.%Y').date()
        if request.form['period'] != '':
            model.period = int(request.form['period'])
        if request.form['departure_date'] != '':
            model.departure_date = datetime.strptime(request.form['departure_date'], '%d.%m.%Y').date()

        if request.form['ticket_price'] != '':
            model.ticket_price = float(request.form['ticket_price'])
        if request.form['club'] != '':
            model.club_id = int(request.form['club'])

        if 'is_accepted_by_root' in request.form:
            if request.form['is_accepted_by_root'] == 'True':
                model.is_accepted_by_root = True
            elif request.form['is_accepted_by_root'] == 'False':
                model.is_accepted_by_root = False

        if 'is_accepted_by_admin' in request.form:
            if request.form['is_accepted_by_admin'] == 'True':
                model.is_accepted_by_admin = True
            elif request.form['is_accepted_by_admin'] == 'False':
                model.is_accepted_by_admin = False

        if model.is_accepted_by_admin is not None and model.is_accepted_by_root is not None and \
                not model.is_accepted_by_root and not model.is_accepted_by_admin:
            avatar = Photo.query.filter_by(id=model.avatar_id).first()
            if avatar is not None:
                db.session.delete(avatar)
            db.session.delete(model)
            db.session.commit()
            print('model has been deleted')
            return redirect(url_for('main.index'))

        db.session.commit()
        return redirect(url_for('main.model', id=model.id))
    return render_template('edit_model.html', model=model, clubs=clubs)


@main.route('/add_photos/<id>', methods=['get', 'post'])
def add_photos(id):
    if request.method == 'POST':
        model = Model.query.filter_by(id=id).first()
        files = dict(request.files)
        if 'photos' in files:
            photos = files['photos']
            for photo in photos:
                print(photo)
                print(photo.filename)
                print(allowed_file(photo.filename))
                if photo != None and photo.filename != '' and allowed_file(photo.filename):
                    filename = secure_filename(photo.filename)
                    file_path = os.path.join(UPLOAD_FOLDER, filename)
                    photo.save(file_path)

                    db_photo = Photo()
                    db_photo.name = filename
                    db_photo.url = file_path
                    db_photo.model_id = model.id

                    db.session.add(db_photo)
            db.session.commit()

        return redirect(url_for('main.model', id=id))
    return render_template('add_photos.html')


@main.route('/delete_model/<id>')
def delete_model(id):
    model = Model.query.filter_by(id=id).first()
    db.session.delete(model)
    db.session.commit()
    return redirect(url_for('main.index'))


@main.route('/create_club', methods=['get', 'post'])
@login_required
def create_club():
    errors = []
    form = AddClubForm()
    if form.validate_on_submit():
        name = form.name.data
        club = Club.query.filter_by(name=name).first()
        if club is not None:
            errors.append('Клуб уже есть в базе')
            return render_template('create_club.html', form=form, errors=errors)
        club = Club()
        club.name = name

        db.session.add(club)
        db.session.commit()
        return redirect(url_for('main.club', id=club.id))

    return render_template('create_club.html', errors=errors, form=form)


@main.route('/edit_club/<id>', methods=['get', 'post'])
def edit_club(id):
    club = Club.query.filter_by(id=id).first()
    if request.method == 'POST':
        name = request.form['name']
        if name != None and name != '':
            club.name = name
            db.session.add(club)
            db.session.commit()

        return redirect(url_for('main.club', id=club.id))
    return render_template('edit_club.html', club=club)


@main.route('/delete_club/<id>')
def delete_club(id):
    club = Club.query.filter_by(id=id).first()
    db.session.delete(club)
    db.session.commit()
    return redirect(url_for('main.index'))


@main.route('/manager/<id>')
def manager(id):
    manager = User.query.filter_by(id=id).first()
    models = manager.models.copy()

    models_archive = []
    for model in models:
        if model.end_date == "В архиве" or model.is_archived:
            models_archive.append(model)
            models.remove(model)

    avatar = Photo.query.filter_by(id=manager.avatar_id).first()
    avatar_name = None
    if avatar is not None:
        avatar_name = avatar.name
    return render_template('manager.html', manager=manager, models=models, models_archive=models_archive,
                           avatar_filename=avatar_name, Photo=Photo)


@main.route('/model/<id>')
def model(id):
    model = Model.query.filter_by(id=id).first()
    avatar = Photo.query.filter_by(id=model.avatar_id).first()
    avatar_name = None
    if avatar is not None:
        avatar_name = avatar.name
    return render_template('model.html', model=model, avatar_filename=avatar_name)


@main.route('/club/<id>')
def club(id):
    club = Club.query.filter_by(id=id).first()
    models = club.models.copy()
    models_archive = []
    for model in models:
        if model.end_date == "В архиве" or model.is_archived:
            models_archive.append(model)
            models.remove(model)
    return render_template('club.html', club=club, models_archive=models_archive, Photo=Photo)

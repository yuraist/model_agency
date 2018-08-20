from flask import render_template, redirect, url_for, request
from flask_login import current_user, login_required

from . import main
from .forms import AddManagerForm, AddModelForm, AddClubForm

from app import db
from app.models import User, Club, Model

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
            new_manager = User()
            new_manager.name = name
            new_manager.username = username
            new_manager.password = password

            # Save him into the database
            db.session.add(new_manager)
            db.session.commit()

        return redirect(url_for('main.manager', id=new_manager.id))
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
    return render_template('manager.html', manager=manager)


@main.route('/model/<id>')
def model(id):
    model = Model.query.filter_by(id=id).first()
    return render_template('model.html', model=model)


@main.route('/club/<id>')
def club(id):
    club = Club.query.filter_by(id=id).first()
    return render_template('club.html', club=club)

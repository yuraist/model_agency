from flask import render_template, redirect, url_for
from flask_login import current_user, login_required

from . import main
from .forms import AddManagerForm, AddModelForm, AddClubForm

from app import db
from app.models import User, Club, Model


@main.route('/')
def index():
    return render_template('main.html')


@main.route('/register_manager', methods=['get', 'post'])
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

        return render_template('manager.html')
    return render_template('register_manager.html', form=form)


@login_required
@main.route('/create_model', methods=['get', 'post'])
def create_model():
    errors = []

    # Get club list
    # clubs = []
    # for club in Club.query.all():
    #     clubs.append(club.name)
    print(1)
    form = AddModelForm()
    if form.validate_on_submit():
        print(2)
        model = Model()
        model.full_name = form.full_name.data
        model.date_of_birth = form.date_of_birth.data
        model.city = form.city.data
        model.phone = form.phone.data
        model.departure_date = form.date_of_birth.data
        model.start_date = form.start_date.data
        model.ticket_price = form.ticket_price.data
        # club_name = form.club.data
        print(3)
        # Find for a club
        # club = Club.query.filter_by(name=club_name).first()
        # if club is None:
        #     errors.append('Не удалось найти клуб')
        #
        # model.club_id = club.id
        model.manager_id = current_user.id

        #TODO: - Implement photo uploading
        db.session.add(model)
        db.session.commit()
        return redirect(url_for('main.model', id=model.id))
    return render_template('create_model.html', form=form, errors=errors)


@main.route('/create_club', methods=['get', 'post'])
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
    return render_template('manager.html', id=id)


@main.route('/model/<id>')
def model(id):
    return render_template('model.html', id=id)


@main.route('/club/<id>')
def club(id):
    return render_template('club.html', id=id)

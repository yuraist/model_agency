from flask import render_template
from flask_login import current_user

from . import main
from .forms import AddManagerForm, AddModelForm, AddClubForm

from app import db
from app.models import User


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
            try:
                db.session.add(manager)
                db.session.commit()
                print(f'Manager {manager.username} has just been created')
            except:
                print('Something went wrong')
        return render_template('manager.html')
    return render_template('register_manager.html', form=form)


@main.route('/create_model', methods=['get', 'post'])
def create_model():
    return render_template('create_model.html')


@main.route('/create_club', methods=['get', 'post'])
def create_club():
    return render_template('create_club.html')


@main.route('/manager/<id>')
def manager(id):
    return render_template('manager.html', id=id)


@main.route('/model/<id>')
def model(id):
    return render_template('model.html', id=id)


@main.route('/club/<id>')
def club(id):
    return render_template('club.html', id=id)

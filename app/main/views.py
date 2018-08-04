from flask import render_template
from . import main


@main.route('/')
def index():
    return render_template('main.html')


@main.route('/manager/<id>')
def manager(id):
    return render_template('manager.html', id=id)


@main.route('/model/<id>')
def model(id):
    return render_template('model.html', id=id)


@main.route('/club/<id>')
def club(id):
    return render_template('club.html', id=id)


@main.route('/register_manager', methods=['get', 'post'])
def register_manager():
    return render_template('register_manager.html')


@main.route('/create_model', methods=['get', 'post'])
def create_model():
    return render_template('create_model.html')


@main.route('/create_club', methods=['get', 'post'])
def create_club():
    return render_template('create_club.html')

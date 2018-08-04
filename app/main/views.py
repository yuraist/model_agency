from flask import render_template
from . import main


@main.route('/')
def index():
    return '<h1>Model Agency</h1>'

# Register
# Login
# Main page
# Create a new manager
# Create a new model
# Create a new club
# Manager’s Profile
# Model’s Profile
# Club Profile


@main.route('/register', methods=['get', 'post'])
def register():
    return '<h1>Registration</h1>'


@main.route('/login', methods=['get', 'post'])
def login():
    return '<h1>Login</h1>'


@main.route('/manager/<id>')
def manager(id):
    return f'<h1>Manager #{id}</h1>'


@main.route('/model/<id>')
def model(id):
    return f'<h1>Model #{id}</h1>'


@main.route('/club/<id>')
def club(id):
    return f'<h1>Club #{id}</h1>'


@main.route('/register_manager', methods=['get', 'post'])
def register_manager():
    return '<h1>Register manager</h1>'


@main.route('/create_model', methods=['get', 'post'])
def create_model():
    return '<h1>Create a new model</h1>'


@main.route('/create_club', methods=['get', 'post'])
def create_club():
    return '<h1>Create a new club</h1>'

from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from . import login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))

    avatar_id = db.Column(db.Integer, db.ForeignKey('photos.id'))

    models = db.relationship('Model', backref='manager')
    archive = db.relationship('Contract', backref='manager', lazy='dynamic')

    # TODO: - Create different roles

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


class Model(db.Model):
    __tablename__ = 'models'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(140))
    date_of_birth = db.Column(db.Date)
    city = db.Column(db.String(64))
    phone = db.Column(db.String(14))
    departure_date = db.Column(db.Date)
    start_date = db.Column(db.Date)
    ticket_price = db.Column(db.Float)
    accepted = db.Column(db.Boolean)

    manager_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    club_id = db.Column(db.Integer, db.ForeignKey('clubs.id'))
    avatar_id = db.Column(db.Integer, db.ForeignKey('photos.id'))

    photos = db.relationship('Photo', backref='model')
    contracts = db.relationship('Contract', backref='model', lazy='dynamic')


class Club(db.Model):
    __tablename__ = 'clubs'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    city = db.Column(db.String(64))

    models = db.relationship('Model', backref='club')


class Photo(db.Model):
    __tablename__ = 'photos'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    url = db.Column(db.String(128))


class Contract(db.Model):
    __tablename__ = 'contracts'
    id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.Date)
    work_period = db.Column(db.Integer)  # Period of work in days
    model_id = db.Column(db.Integer, db.ForeignKey('models.id'))
    club_id = db.Column(db.Integer, db.ForeignKey('clubs.id'))
    manager_id = db.Column(db.Integer, db.ForeignKey('users.id'))

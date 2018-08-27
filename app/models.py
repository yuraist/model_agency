from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from . import login_manager

from datetime import datetime


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Permission:
    CREATE_MODEL = 1
    SEE_MODEL = 2
    CREATE_MANAGER = 4
    ADMINISTER = 64


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    permissions = db.Column(db.Integer)
    default = db.Column(db.Boolean, default=False, index=True)

    # Relations
    users = db.relationship('User', backref='role', lazy='dynamic')

    @staticmethod
    def insert_roles():
        roles = {
            'Manager': [Permission.CREATE_MODEL],
            'Administrator': [Permission.CREATE_MODEL, Permission.CREATE_MANAGER,
                              Permission.SEE_MODEL, Permission.ADMINISTER]
        }

        default_role = 'Administrator'
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role()
                role.name = r
            role.reset_permission()
            for perm in roles[r]:
                role.add_permission(perm)
            role.default = (role.name == default_role)
            db.session.add(role)
        db.session.commit()

    def add_permission(self, perm):
        if not self.has_permission(perm):
            self.permissions += perm

    def remove_permission(self, perm):
        if self.has_permission(perm):
            self.permissions -= perm

    def reset_permission(self):
        self.permissions = 0

    def has_permission(self, perm):
        return self.permissions & perm == perm


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))

    is_root = db.Column(db.Boolean, default=False)
    is_admin = db.Column(db.Boolean, default=False)

    # Relations
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    avatar_id = db.Column(db.Integer, db.ForeignKey('photos.id'))
    models = db.relationship('Model', backref='manager')
    archive = db.relationship('Contract', backref='manager', lazy='dynamic')

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
    next_date = db.Column(db.Date)
    ticket_price = db.Column(db.Float)
    is_accepted_by_admin = db.Column(db.Boolean)
    is_accepted_by_root = db.Column(db.Boolean)
    period = db.Column(db.Integer)
    is_archived = db.Column(db.Boolean, default=False)

    # Relations
    manager_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    club_id = db.Column(db.Integer, db.ForeignKey('clubs.id'))
    avatar_id = db.Column(db.Integer, db.ForeignKey('photos.id'))
    photos = db.relationship('Photo', backref='model')
    contracts = db.relationship('Contract', backref='model', lazy='dynamic')

    @property
    def end_date(self):
        if self.start_date is not None and self.period is not None:
            delta = datetime.utcnow().date() - self.start_date
            if delta.days <= 0:
                return self.period
            elif (delta.days > 0) and (delta.days < self.period):
                return self.period - delta.days
            else:
                self.is_archived = True
                return 'В архиве'
        return '-'


class Club(db.Model):
    __tablename__ = 'clubs'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True)

    # Relations
    models = db.relationship('Model', backref='club')

    def __repr__(self):
        return self.name


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

    # Relations
    model_id = db.Column(db.Integer, db.ForeignKey('models.id'))
    club_id = db.Column(db.Integer, db.ForeignKey('clubs.id'))
    manager_id = db.Column(db.Integer, db.ForeignKey('users.id'))

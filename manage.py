import os

# Importing environment variables from the .env file
if os.path.exists('.env'):
    print('Importing environment from .env...')
    for line in open('.env'):
        var = line.strip().split('=')
        if len(var) == 2:
            os.environ[var[0]] = var[1]

from app import create_app
from app.models import *
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

app = create_app(os.environ.get('CONFIG'))

manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, Model=Model, User=User, Photo=Photo)


manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


@manager.command
def deploy():
    from flask_migrate import upgrade

    upgrade()
    Role.insert_roles()


if __name__ == '__main__':
    manager.run()

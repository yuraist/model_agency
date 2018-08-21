import os
base_dir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = str(os.environ.get('DATABASE_URL'))

    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')

    # Uploading images
    UPLOAD_FOLDER = os.path.join(base_dir, 'app/static/images')

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = True
    TEMPLATES_AUTO_RELOAD = True


config = {
    'dev': DevelopmentConfig,
    'prod': Config,
    'default': DevelopmentConfig
}


ALLOWED_EXTENSIONS = ('png', 'jpg', 'jpeg', 'gif')


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

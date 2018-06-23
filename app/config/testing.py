import os


class TestingConfig:
    DEBUG = True
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    DATABASE_LOCATION = os.path.join(BASE_DIR, 'test.db')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(DATABASE_LOCATION)
    SQLALCHEMY_TRACK_MODIFICATIONS = False

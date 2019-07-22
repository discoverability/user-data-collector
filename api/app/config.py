import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SQLALCHEMY_DATABASE_URI = "postgresql://{}:{}@db:5432/discoverability".format(
        os.environ.get('POSTGRES_USER'),
        os.environ.get('POSTGRES_PASSWORD')
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

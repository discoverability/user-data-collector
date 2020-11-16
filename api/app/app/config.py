import os

basedir = os.path.abspath(os.path.dirname(__file__))


class DevConfig(object):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    DEVELOPMENT = True
    DEBUG = True
    SECRET_KEY = 'EMNS2606!'
    SQLALCHEMY_RECORD_QUERIES = False
    SQLALCHEMY_ECHO = True
    CACHE_TYPE = "simple"  # Flask-Caching related configs


class ProdConfig(object):
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    DEVELOPMENT = False
    DEBUG = False  # some Flask specific configs
    SECRET_KEY = 'EMNS2606!'
    SQLALCHEMY_ECHO = False

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {"pool_size": 100, "max_overflow": 100, "pool_recycle": 280}

    CACHE_TYPE = os.environ.get("CACHE_TYPE", "redis")  # Flask-Caching related configs
    CACHE_DEFAULT_TIMEOUT = 300
    CACHE_KEY_PREFIX = "conso-api"
    CACHE_REDIS_URL = os.environ.get("CACHE_REDIS_URL", "")


env = os.environ.get("APP_ENV", "development")
print("[CONSO-API] environment : %s" % env)
if env == "production":
    config = ProdConfig()
else:
    config = DevConfig()
print("[CONSO-API] using %s config " % str(type(config)))

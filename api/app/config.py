import os
basedir = os.path.abspath(os.path.dirname(__file__))

class DevConfig(object):
    SQLALCHEMY_DATABASE_URI='sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS=True
    DEVELOPMENT=True
    DEBUG=True


class ProdConfig(object):
    SQLALCHEMY_DATABASE_URI= "mysql://discoverability:aWuathigh8Ui@ts236797-001.dbaas.ovh.net:35824/discoverability"
    DEVELOPMENT=False
    DEBUG=False
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    SQLALCHEMY_ENGINE_OPTIONS={"pool_size":100,"max_overflow":100}


env=os.environ.get("APP_ENV","development")
print("environment : %s"%env)
if(env=="production"):
    config=ProdConfig()
else:
    config=DevConfig()

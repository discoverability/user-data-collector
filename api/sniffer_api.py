import os
basedir = os.path.abspath(os.path.dirname(__file__))
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

application = Flask(__name__)
application.config["SQLALCHEMY_DATABASE_URI"]='sqlite:///' + os.path.join(basedir, 'app.db')
#application.config["SQLALCHEMY_DATABASE_URI"]="mysql://discoverability:aWuathigh8Ui@ts236797-001.dbaas.ovh.net:35824/discoverability"
application.config["DEVELOPMENT"]=True
application.config["DEBUG"]=True
CORS(application)
db = SQLAlchemy(application)
migrate = Migrate(application, db)
from app import routes, models, modelsgen

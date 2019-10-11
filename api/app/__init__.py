from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
import os
basedir = os.path.abspath(os.path.dirname(__file__))
from app.config import config


app = Flask(__name__)
CORS(app)
app.config.from_object(config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import routes, models, modelsgen

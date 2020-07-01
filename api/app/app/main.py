import sys
import os
from flask import Flask
from flask_debugtoolbar import DebugToolbarExtension
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_caching import Cache

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.jinja_env.add_extension('jinja2.ext.do')
CORS(app)

from app.config import config

app.config.from_object(config)
cache = Cache(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
toolbar = DebugToolbarExtension(app)

#from app.routes import *
from app.dataviz_api import *

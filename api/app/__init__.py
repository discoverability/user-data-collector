from flask import Flask
from flask_debugtoolbar import DebugToolbarExtension
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
import os
basedir = os.path.abspath(os.path.dirname(__file__))
from app.config import config


app = Flask(__name__)
#app.jinja_options['extensions'].append('jinja2.ext.do')

app.jinja_env.add_extension('jinja2.ext.do')
CORS(app)
app.config.from_object(config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

toolbar = DebugToolbarExtension(app)
from app import routes, models, dataviz_api

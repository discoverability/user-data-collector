import sys
import os
from werkzeug.middleware.proxy_fix import ProxyFix
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
ProxyFix(app.wsgi_app, x_for=1, x_host=1)
execution_context = os.environ.get("EXECUTION_CONTEXT", "conso-api;api")
execution_contexts = execution_context.split(";")
if "conso-api" in execution_contexts:
	from app.routes import *
	from app.direct_schedule_api import *
if "api" in execution_contexts:
	from app.dataviz_api import *
	from app.datavis_custom import *

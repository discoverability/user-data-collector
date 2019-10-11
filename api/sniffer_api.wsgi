import sys
sys.path.insert(0, '/var/www/discoverability/api')

from app import app as application
application.config.from_object("app.config.ProductionConfig")
CORS(application)


from paste.evalexception.middleware import EvalException
application = EvalException(application)


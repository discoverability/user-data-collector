import sys
sys.path.insert(0, '/var/www/discoverability/api')

from app import app as application

from paste.evalexception.middleware import EvalException
application = EvalException(application)


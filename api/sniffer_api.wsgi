import sys
sys.path.insert(0, '/var/www/discoverability/api')

import app
from app.config import ProdConfig as config
from app import app as application
application.config.from_object(config)

from paste.evalexception.middleware import EvalException
application = EvalException(application)


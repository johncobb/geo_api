

import os

# Statement for enabling the development environment
DEBUG = True

# Define the application directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Define route prefix for subdirectory routing
ROUTE_PREFIX = os.getenv('ROUTE_PREFIX', '')
print "ROUTE_PREFIX = ", ROUTE_PREFIX

# Define the database - we are working with
# SQLite for this example

# Rackspace UNI-DB-HA-01 (High Availability)
#SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://scanner_user:2Wsxdr5!@652b5aa36db04193b089433872471075.publb.rackspaceclouddb.com/Scanner'

# Rackspace UNI-DB-HA-01 (High Availability) **** DEVELOPMENT DATABASE ***
#SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://dev_scanner_user:2Wsxdr5!@652b5aa36db04193b089433872471075.publb.rackspaceclouddb.com/DevScanner'

#SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

SQLALCHEMY_DATABASE_URI = os.getenv('DB_URI', 'sqlite:///:memory:')
DB_ENV = os.getenv('DB_ENV', 'memory')
print "DB_ENV = ", DB_ENV
print "SQLALCHEMY_DATABASE_URI = ", SQLALCHEMY_DATABASE_URI
if DB_ENV == 'mysql' :
    SQLALCHEMY_ECHO = False # Log all output to stderr
    DB_ENV="memory"
    SQLALCHEMY_POOL_SIZE = 4
    #SQLALCHEMY_POOL_TIMEOUT = 10
    SQLALCHEMY_POOL_RECYCLE = 3600 


REDIS_QUEUE_URL = os.environ['REDIS_QUEUE_URL']
REDIS_QUEUE_PORT = os.environ['REDIS_QUEUE_PORT']

#REDIS_QUEUE = redis.Redis(host=REDIS_QUEUE_URL, port=REDIS_QUEUE_PORT)

DATABASE_CONNECTION_OPTIONS = {}
# Application threads. A common general assumption is
# using 2 per available processor cores - to handle
# incoming requests using one and performing background
# operations using the other.
THREADS_PER_PAGE = 2

# Enable protection agains *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED = True

# Use a secure, unique and absolutely secret key for
# signing the data.
CSRF_SESSION_KEY = 'secret'

# Secret key for signing cookies
SECRET_KEY = 'followtheyellowbrickroad'



UPLOAD_FOLDER = 'templates'
ALLOWED_EXTENSIONS = {'zpl'}
OAUTH_API_KEY_ID = 'P7BB0S5LDFQAB9S7T7G8D9BWX'
OAUTH_API_KEY_SECRET = 'XBsujgy0eapQtzaTMs+am/g1m7xf7SaRlV1ErgL//rg'

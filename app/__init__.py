

import os
import jwt
import json
from functools import wraps, update_wrapper
from flask import Flask, _app_ctx_stack
from flask_cors import cross_origin
from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
from flask import request, redirect, url_for, render_template
from werkzeug.security import safe_str_cmp
from flask_cors import CORS, cross_origin

# Custom JSON returns
class JSON_API_Message:
    JSON_200_OK = {"200":"OK"}
    JSON_204_NO_CONTENT = {"204": "NO CONTENT"}
    JSON_400_BAD_REQUEST = {"400": "BAD REQUEST"}

class Payload(object):
    def __init__(self, j):
        self.__dict__ = json.loads(j)["data"]

class ApiExceptionHandler(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload 
    def to_dict(self):
        rv = dict(self.payload or ())
        rv['exception'] = self.message
        return rv

# http://stackoverflow.com/questions/18967441/add-a-prefix-to-all-flask-routes/18969161#18969161
class PrefixMiddleware(object):
    
    def __init__(self, app, prefix=''):
        self.app = app
        self.prefix = prefix

    def __call__(self, environ, start_response):
        if environ['PATH_INFO'].startswith(self.prefix):
            environ['PATH_INFO'] = environ['PATH_INFO'][len(self.prefix):]
            environ['SCRIPT_NAME'] = self.prefix
            return self.app(environ, start_response)
        else:
            start_response('404', [('Content-Type', 'text/plan')])
            return ["This url does not belong to the app".encode()]

app = Flask(__name__)

# Setup static path for Flask to render from
static_path = os.path.join(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'), 'static')
app._static_folder = static_path

# Configuration
app.config.from_object('config')

# Attach middleware and wrappers
app.wsgi_app = PrefixMiddleware(app.wsgi_app, app.config['ROUTE_PREFIX'])
CORS(app)

@app.errorhandler(ApiExceptionHandler)
def handle_api_exception(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

@app.route('/home')
def index():
    return render_template('index.html')

@app.route('/foo')
def get_foo():
    raise ApiExceptionHandler('Foo has gone awry!', status_code=410)

# Format error response and append status code.
def handle_error(error, status_code):
    resp = jsonify(error)
    resp.status_code = status_code
    return resp

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):


        client_id = '496priyO44FWmZu5YQ27s6AJDJmQU702'
        #client_secret ='jUwAL_nTmeZXtflz6SaIj905_9VHzkKMMEThtLYdh5i7voDmR7f66mL_RGZYRN82'
        client_secret = 'eii9DI0vgvORyPMkxaaoHDZIt3RA-IePcChK6uD3_be39iVEzVWUDs2aZy-D9iLc'
        auth = request.headers.get('Authorization', None)
        if not auth:
            return handle_error({'code': 'authorization_header_missing',
                                'description':
                                    'Authorization header is expected'}, 401)

        parts = auth.split()

        if parts[0].lower() != 'bearer':
            return handle_error({'code': 'invalid_header',
                                'description':
                                    'Authorization header must start with'
                                    'Bearer'}, 401)
        elif len(parts) == 1:
            return handle_error({'code': 'invalid_header',
                                'description': 'Token not found'}, 401)
        elif len(parts) > 2:
            return handle_error({'code': 'invalid_header',
                                'description': 'Authorization header must be'
                                 'Bearer + \s + token'}, 401)

        token = parts[1]
        try:
            payload = jwt.decode(
                token,
                client_secret,
                audience=client_id
            )
            print payload
        except jwt.ExpiredSignature:
            return handle_error({'code': 'token_expired',
                                'description': 'token is expired'}, 401)
        except jwt.InvalidAudienceError:
            return handle_error({'code': 'invalid_audience',
                                'description': 'incorrect audience, expected: '
                                 + client_id}, 401)
        except jwt.DecodeError:
            return handle_error({'code': 'token_invalid_signature',
                                'description':
                                    'token signature is invalid'}, 401)
        except Exception:
            return handle_error({'code': 'invalid_header',
                                'description': 'Unable to parse authentication'
                                 ' token.'}, 400)

        _app_ctx_stack.top.current_user = payload
        return f(*args, **kwargs)

    return decorated

# No auth required
@app.route('/ping')
@cross_origin(headers=['Content-Type', 'Authorization'])
def ping():
    return "Good to go"

# Auth required
@app.route('/secured/ping')
@cross_origin(headers=['Content-Type', 'Authorization'])
@requires_auth
def securedPing():
    return "Good to go, you're authenticated"

# Setup static path for Flask to render from
#static_path = os.path.join(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'), 'static')
#app._static_folder = static_path

# Configuration
#app.config.from_object('config')


# Define database object
db = SQLAlchemy(app)

from app.mod_organization.controllers.application import bp_app as bp_app_module
from app.mod_organization.controllers.applet import bp_applet as bp_applet_module
from app.mod_organization.controllers.organization import bp_organization as bp_organization_module
from app.mod_organization.controllers.user import bp_user as bp_user_module
from app.mod_organization.controllers.group import bp_group as bp_group_module

from app.mod_geo.controllers.landmark import bp_landmark as bp_geo_landmark
from app.mod_geo.controllers.geofence import bp_geofence as bp_geo_fence

app.register_blueprint(bp_app_module)
app.register_blueprint(bp_applet_module)
app.register_blueprint(bp_organization_module)
app.register_blueprint(bp_user_module)
app.register_blueprint(bp_group_module)

app.register_blueprint(bp_geo_landmark)
#app.register_blueprint(bp_scanner_applet_module)
app.register_blueprint(bp_geo_fence)
db.create_all()

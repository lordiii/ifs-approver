from functools import wraps
import json
from functools import update_wrapper

from flask import Response
from flask import make_response, request, current_app

from ifsApprover import db


def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    return db.check_login(username, password)


def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
        'Could not verify your access level for that URL.\n'
        'You have to login with proper credentials', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'})


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)

    return decorated


def copy_fields(db_row, fields):
    result = {}
    for key in fields:
        result[key] = db_row[key]
    return result


def make_json_response(data={}, status="ok"):
    data = json.dumps({
        "status": status,
        "data": data
    })
    return Response(data, mimetype='application/json')


# some parts from http://flask.pocoo.org/snippets/56/
def crossdomain(methods=None, headers=None,
                attach_to_all=True,
                automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, basestring):
        headers = ', '.join(x.upper() for x in headers)

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers
            h['Access-Control-Allow-Credentials'] = "true"
            h['Access-Control-Allow-Origin'] = request.headers.get("Origin", "*")
            h['Access-Control-Allow-Methods'] = get_methods()
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)

    return decorator
"""A simple flask app to create a JWT

    Usage: main.py

Attributes:
    JWT_SECRET: A str constrant environmental variable representing the
        encryption secret for JWTs (default: abc123abc123)
    LOG_LEVEL: A str constant environmental variable representing what level to
        log at (default: INFO)
    logger: A logging object representing the logger
    app: A flask Flask object creating the flask app
"""

import os
import logging
import datetime
import functools
import jwt
from flask import Flask, jsonify, request, abort

JWT_SECRET = os.environ.get('JWT_SECRET', 'abc123abc1234')
LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')


def _logger():
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    log = logging.getLogger(__name__)
    log.setLevel(LOG_LEVEL)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    log.addHandler(stream_handler)

    return log


logger = _logger()
logger.debug('Starting with log level: %(LOG_LEVEL)s')
app = Flask(__name__)


def require_jwt(function):
    """A decorator to check if a valid JWT is present with the request"""

    @functools.wraps(function)
    def decorated_function(*args, **kws):
        if 'Authorization' not in request.headers:
            abort(401)

        data = request.headers['Authorization']
        token = str.replace(str(data), 'Bearer ', '')

        try:
            jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
        except Exception:  # pylint: disable=broad-except
            abort(401)

        return function(*args, **kws)

    return decorated_function


@app.route('/', methods=['POST', 'GET'])
def health():
    """The route handler for the home page

    Returns:
        A simple health check that returns the str 'Healthy'
    """
    return jsonify('Healthy')


@app.route('/auth', methods=['POST'])
def auth():
    """Create a JWT based on the provided email, password, and secret

    Returns:
        token: A str representing a JWT
    """

    request_data = request.get_json()
    email = request_data.get('email')
    password = request_data.get('password')

    if not email:
        logger.error('No email provided')
        return jsonify({
            'message': 'Missing parameter: email'
        }, 400)

    if not password:
        logger.error('No password provided')
        return jsonify({
            'message': 'Missing parameter: password'
        }, 400)

    body = {
        'email': email,
        'password': password
    }

    user_data = body
    token = jsonify(token=_get_jwt(user_data).decode('utf-8'))

    return token


@app.route('/contents', methods=['GET'])
def decode_jwt():
    """Decode a user token

    Returns:
        response: A dict representing the non-secret data from the JWT
    """

    if 'Authorization' not in request.headers:
        abort(401)

    data = request.headers['Authorization']
    token = str.replace(str(data), 'Bearer ', '')

    try:
        data = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
    except Exception:  # pylint: disable=broad-except
        abort(401)

    response = {
        'email': data['email'],
        'exp': data['exp'],
        'nbf': data['nbf']
    }

    return jsonify(**response)


def _get_jwt(user_data):
    exp_time = datetime.datetime.utcnow() + datetime.timedelta(weeks=2)
    payload = {
        'exp': exp_time,
        'nbf': datetime.datetime.utcnow(),
        'email': user_data['email']
    }

    return jwt.encode(payload, JWT_SECRET, algorithm='HS256')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)

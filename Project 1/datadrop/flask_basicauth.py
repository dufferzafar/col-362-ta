"""
    flask.ext.basicauth
    ~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2013 Janne Vanhala.
    :license: BSD, see LICENSE for more details.

    https://github.com/jpvanhal/flask-basicauth/blob/master/flask_basicauth.py
"""
import base64
from functools import wraps

from flask import current_app, request, Response


__version__ = '0.2.0'


class BasicAuth(object):
    def __init__(self, app=None):
        if app is not None:
            self.app = app
            self.init_app(app)
        else:
            self.app = None

    def init_app(self, app):
        app.config.setdefault('BASIC_AUTH_FORCE', False)
        app.config.setdefault('BASIC_AUTH_REALM', '')

        @app.before_request
        def require_basic_auth():
            if not current_app.config['BASIC_AUTH_FORCE']:
                return
            if not self.authenticate():
                return self.challenge()

    def check_credentials(self, username, password):
        correct_username = current_app.config['BASIC_AUTH_USERNAME']
        correct_password = current_app.config['BASIC_AUTH_PASSWORD']
        return username == correct_username and password == correct_password

    def authenticate(self):
        auth = request.authorization
        return (
            auth and auth.type == 'basic' and
            self.check_credentials(auth.username, auth.password)
        )

    def challenge(self):
        realm = current_app.config['BASIC_AUTH_REALM']
        return Response(
            status=401,
            headers={'WWW-Authenticate': 'Basic realm="%s"' % realm}
        )

    def required(self, view_func):
        @wraps(view_func)
        def wrapper(*args, **kwargs):
            if self.authenticate():
                return view_func(*args, **kwargs)
            else:
                return self.challenge()
        return wrapper

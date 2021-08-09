from functools import wraps
from flask import Response, request, g
from werkzeug.wrappers import Request, Response, ResponseStream

def jwt_verify(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        
        username = request.authorization['username']
        password = request.authorization['password']

        if username == 'TestUser' and password == 'TestPass':
            token = 'test token here!'

            g.token = token

            return func(*args, **kwargs)

        return Response('Authorization failed', mimetype='text/plain', status=401)

    return decorated_function
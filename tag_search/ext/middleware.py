from functools import wraps
from flask import Response, request, g
from werkzeug.wrappers import Response
from ext.jwt import jwt_handler

def jwt_verify(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
    
        if request.authorization is not None:
            auth_token = request.authorization.split(' ')[1]
        elif request.cookies.get('token') is not None:
            auth_token = request.cookies.get('token')
        else:
            auth_token = None

        if auth_token is not None:
            
            token = jwt_handler.get_jwt_decode(auth_token)
        
            if token is not None and token.get('error') is None:
                g.token = token
                return func(*args, **kwargs)

        return Response('Authorization failed, please log again', mimetype='text/plain', status=401)

    return decorated_function


def auth_verify(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        
        if request.authorization is not None:
            username = request.authorization['username']
            password = request.authorization['password']

        elif request.form is not None:
            username = request.form['username']
            password = request.form['password']
        
        #if userModule.auth(username, password) is not None:
        if username is not None and password is not None:

            return func(*args, **kwargs)

        return Response('Authorization failed, please log again', mimetype='text/plain', status=401)

    return decorated_function
import jwt, datetime,os
from flask import current_app

class jwt_handler():

    @staticmethod
    def get_jwt_encode (dict):
        return jwt.encode(dict, current_app.config['JWT_SECRET_KEY'], algorithm="RS256")


    @staticmethod
    def get_jwt_decode (str):
        try:
            return jwt.decode(str, current_app.config['JWT_PUBLIC_KEY'], algorithms=["RS256"])
        except jwt.ExpiredSignatureError:
            return { 'error' :'Signature expired. Please log in again.'}
        except jwt.InvalidTokenError:
            return { 'error' :'Invalid token. Please log in again.'}
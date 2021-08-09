
import jwt, datetime,os

class jwt_handler():

    @staticmethod
    def get_jwt_encode (self,dict):
        dict["exp"] = datetime.datetime.utcnow() + datetime.timedelta(hours=4)    
        return jwt.encode(dict, os.getenv("JWT_TOKEN"), algorithm="HS256")


    @staticmethod
    def get_jwt_decode (self,str):
        try:
            return jwt.decode(str, os.getenv("JWT_TOKEN"), algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'
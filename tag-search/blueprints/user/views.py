import re , datetime
from sqlalchemy.orm import query_expression, session
from werkzeug.utils import redirect

from .user import User
from flask import Flask, render_template, jsonify, request, Response, url_for,Blueprint, render_template, make_response
from flask.json import jsonify

from sqlalchemy.sql.expression import update
from sqlalchemy.sql import text
from sqlalchemy.exc import DatabaseError, DataError
from ...ext.models import  Places, Session ,set_user_session
from ...blueprints import user as userModule
from ..place.place import Place
from ...ext.cache import cache
from ...ext.utils import utils
from ...ext.jwt import jwt_handler
from ...ext.redis import db_cache
from ...ext.constants import cache_time
from ...ext.middleware import auth_verify, jwt_verify


user = Blueprint('user', __name__,
                    template_folder="../templates", url_prefix="/user")

#TODO CRUD for users
@user.route('/auth/', methods=['POST'], strict_slashes=False)
@auth_verify
def auth():
    
    if request.authorization is not None:
        username = request.authorization['username']
        password = request.authorization['password']
    else:
        username = request.form['username']
        password = request.form['password']


    valid_user = User().auth(username,password)

    if valid_user is None :
        return render_template('admin.html',error='Invalid Credentials')

    token = jwt_handler.get_jwt_encode({
        'id' : valid_user[0],
        'sub' : valid_user[0],
        'is_admin' : valid_user[4],
        'iat' : datetime.datetime.utcnow() + datetime.timedelta(hours=3),
        'exp' : datetime.datetime.utcnow() + datetime.timedelta(hours=4)
    })
    
    db_cache().conn().set(utils.get_hash(token),'',ex=cache_time.ONE_HOUR)
        
    resp = make_response(render_template('auth.html'))
    expire_time = datetime.datetime.utcnow() + datetime.timedelta(hours=4)
    resp.set_cookie(key='token', value=token,expires=expire_time)

    return resp

@user.route('/home/', methods=['GET'], strict_slashes=False)
@jwt_verify
def home():
    data = {}
    places = Place().get_place_all()
    if places :        
        data['places_keys'] = places[0]._fields,
        data['places'] = places

    return render_template('home.html',data=data)

@user.route('/admin/', methods=['GET'], strict_slashes=False)
@cache.cached(timeout=cache_time.END_CURRENT_DAY, query_string=True)
def admin():
    return render_template('admin.html')
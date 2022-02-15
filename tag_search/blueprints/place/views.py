import re

from sqlalchemy.exc import DatabaseError, DataError
from .place import Place
from flask import jsonify, request
from flask.json import jsonify
from sqlalchemy import exc
from ext.cache import cache
from ext.utils import utils
from ext.constants import cache_time, regex_pattern
from ext.middleware import jwt_verify
from flask import Blueprint

place = Blueprint('place', __name__,
                    template_folder="../templates", url_prefix="/place")

@place.route('/', methods=['GET'], strict_slashes=False)
@place.route('/<int:id>', methods=['GET'], strict_slashes=False)
@place.route('/<string:tags>/', methods=['GET'], strict_slashes=False)
@cache.cached(timeout=cache_time.END_CURRENT_DAY, query_string=True)
def get_place(id=None,tags=None):

    if (id is None and tags is None):

        result = Place.get_place_all()

    elif id is not None:

        result = Place.get_place_by_id(id)

    elif tags is not None and not re.search(regex_pattern.NON_WORDS, tags.replace(',', '')):
        result = Place.get_place_by_tags(tags)

    query = utils.result2dict(result) if result is not None and len(result) > 0 else None
    
    return jsonify(query)

@place.route('/<int:id>', methods=['DELETE'], strict_slashes=False)
@jwt_verify
def del_place(id):

    try:
        Place.delete(id)
        cache.clear()
        return jsonify({"result": True})
        
    except DataError as e:
        raise DataError('Erro to delete place' + str(e.args[0]), 500)

@place.route('/', methods=['POST'], strict_slashes=False)
@jwt_verify
def ins_place():

    try:
        if not request.is_json:
            raise DataError('Error to add place, invalid input', 400)

        data = request.get_json()
        Place.insert(data)
        cache.clear()
        return jsonify({"result": True})
    except exc.IntegrityError as e:
        raise DataError(
            'Error to insert place, invalid payload. ' + str(e.args[0]), 400)
    except DataError as e:
        raise DataError(
            'Error to insert place, invalid payload. ' + str(e.args[0]), 400)
    except DatabaseError as e:
        raise DatabaseError(
            'Error to insert place ' + str(e.args[0]), 400)

@place.route('/', methods=['PUT', 'PATCH'], strict_slashes=False)
@jwt_verify
def upd_place():
    try:
        if not request.is_json:
            raise DataError(
                'Error to update place, invalid payload. ', 400)

        data = request.get_json()

        if data['id'] is None:
            raise DataError(
                'Error to insert place, invalid id. ', 400)

        Place.update(data)
        cache.clear()
        return jsonify({"result": True})

    except DataError as e:
        raise DataError('Error to update place. ' + str(e.args[0]), 500)
    except DatabaseError as e:
        raise DatabaseError(
            'Error to insert place ' + str(e.args[0]), 400)
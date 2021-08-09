import re

from sqlalchemy.orm import query_expression
from .contact import Contact
from flask import Flask, render_template, jsonify, request, Response
from flask.json import jsonify
from redis import DataError
from sqlalchemy.sql.expression import update
from sqlalchemy.sql import text
from sqlalchemy import exc
from ...ext.models import Contactstags, Session, Contacts, Tag, set_user_session
from ...ext.cache import cache
from ...ext.utils import utils
from ...ext.redis import db_cache
from ...ext.constants import cache_time, regex_pattern
from flask import Blueprint, render_template

contact = Blueprint('contact', __name__,
                    template_folder="../templates", url_prefix="/contact")


@cache.cached(timeout=3600, query_string=True)
@contact.route('/', methods=['GET'], strict_slashes=False)
@contact.route('/<int:id>', methods=['GET'], strict_slashes=False)
@contact.route('/<string:tags>/', methods=['GET'], strict_slashes=False)
def get_contact(id=None,tags=None):


    session = Session()

    if (id is None and tags is None):

        result = Contact.get_contact_all(session)

    elif id is not None:

        result = Contact.get_contact_by_id(session,id)

    elif tags is not None:

        result = Contact.get_contact_by_tags(session,tags)

    key = result["key"]        
    query = result["query"]

    expire_time = (cache_time.ONE_HOUR,cache_time.END_CURRENT_DAY)[tags is None]
    result = utils.result2dict(query)
    db_cache.conn().setex(key, expire_time, utils.dict2str(result))

    return jsonify(result)


@contact.route('/<int:id>', methods=['DELETE'], strict_slashes=False)
def del_contact(id):

    try:
        session = Session()
        session.begin()
        Contact.delete(session,id)
        return jsonify({"result": True})
        
    except DataError as e:
        session.rollback()
        raise DataError('Erro to delete contact' + str(e.args[0]), 500)
    finally:
        session.close()


@contact.route('/', methods=['POST'], strict_slashes=False)
def ins_contact():

    try:
        if not request.is_json:
            raise DataError('Error to add contact, invalid input', 400)

        data = request.get_json()
        id_user = 1
        session = Session()
        Contact.insert(session,data,id_user)
        keys = 'ts_contact_0'
        db_cache.conn().delete(keys)
        return jsonify({"result": True})
    except exc.IntegrityError as e:
        session.rollback()
        raise DataError(
            'Error to insert contact, invalid payload. ' + str(e.args[0]), 400)
    except DataError as e:
        session.rollback()
        raise DataError(
            'Error to insert contact, invalid payload. ' + str(e.args[0]), 400)
    finally:
        session.close()


@contact.route('/', methods=['PUT', 'PATCH'], strict_slashes=False)
def upd_contact():
    try:
        if not request.is_json:
            raise DataError(
                'Error to update contact, invalid payload. ', 400)

        data = request.get_json()

        if data['id'] is None:
            raise DataError(
                'Error to insert contact, invalid id. ', 400)

        session = Session()

        id_user = '1'
        Contact.update(session,data,id_user)

        keys = ['ts_contact_' + str(data['id']), 'ts_contact_0']
        db_cache.delete_many_keys(keys)

    except DataError as e:
        session.rollback()
        raise DataError('Error to update contact. ' + str(e.args[0]), 500)
    finally:
        session.close()
    return jsonify({"result": True})


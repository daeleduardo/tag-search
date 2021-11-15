import json,re
from sqlalchemy.sql import text
from sqlalchemy.sql.expression import update
from sqlalchemy.exc import DatabaseError, DataError
from ...ext.redis import db_cache
from ...ext.constants import regex_pattern
from ...ext.utils import utils
from ...ext.models import Placestags, Session, Places, Tags, set_user_session

#TODO write a user CRUD
class User():

    @staticmethod
    def auth(user, pwd):

        session = Session()

        sql = text("""
        select
            id_users,
            name,
            email,
            password,
            is_admin
        from
            users
        where
            email = :email
            and password = :password
            and is_active = :is_active
        """)

        query = session.execute(sql,
            {'email': user,
            'password': utils.get_hash(pwd, only_numeric=False),
            'is_active':True}
            ).first()

        return query
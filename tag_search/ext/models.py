import os, datetime
from unicodedata import category

from sqlalchemy.sql.sqltypes import DECIMAL, BigInteger


from constants import env
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.schema import Index, UniqueConstraint, ForeignKey
from sqlalchemy import Column, String, Integer, Boolean, DateTime, Index, create_engine
from dotenv import load_dotenv
from flask import g

load_dotenv()

if os.getenv("FLASK_ENV") == env.PRODUCTION  :
    db_string = os.getenv("DB_PROD_URI") 
elif os.getenv("FLASK_ENV") == env.TEST : 
    db_string = os.getenv("DB_TEST_URI")
elif os.getenv("FLASK_ENV") == env.MEMORY :
    db_string = "sqlite:///databases/temp.db"
engine = create_engine(db_string, echo=True, echo_pool='debug')
base = declarative_base()
Session = sessionmaker(bind=engine,autocommit=False,autoflush=False)

def set_user_session(session,id):
    return
    if isinstance(id,int):
        return session.execute("set users.id to '"+str(id)+"';")
    raise TypeError("set_user_session: id must be an integer")
    
def get_user_id():
    try:
        return g.token['id']
    except RuntimeError:
        return 0
        

class Placestags(base):
    __tablename__ = 'places_tags'

    id_place_tag = Column('id_places_tags', Integer, primary_key=True,autoincrement=True)
    id_tag = Column('id_tags', Integer, ForeignKey('tags.id_tags'), index=True)
    id_place = Column('id_places', Integer, ForeignKey('places.id_places'), index=True)

    Index("idx_place_tag", id_tag, id_place)
    UniqueConstraint('id_tags', 'id_places', name='places_tags')


class Places(base):
    __tablename__ = 'places'

    id_places = Column('id_places', Integer, primary_key=True,autoincrement=True)
    name = Column('name', String(100), nullable=False, index=True)
    category = Column('category', String(100), nullable=False, index=True)
    latitude = Column('latitude', DECIMAL(precision=18,scale=15), nullable=False)
    longitude = Column('longitude', DECIMAL(precision=18,scale=15), nullable=False)
    id_create = Column('id_create', Integer, nullable=True, default=get_user_id)
    create_at = Column('create_at', DateTime, nullable=True, default=datetime.datetime.now)
    id_update = Column('id_update', Integer, nullable=True, onupdate=get_user_id)
    update_at = Column('update_at', DateTime, nullable=True, onupdate=datetime.datetime.now)
    placestags = relationship("Placestags",backref='places')


class Tags(base):
    __tablename__ = 'tags'

    id_tags = Column('id_tags', Integer, primary_key=True,autoincrement=True)
    name = Column('name', String(100), nullable=False, unique=True)
    hash_name = Column('hash_name', BigInteger, nullable=False, index=True)
    id_create = Column('id_create', Integer, nullable=True, default=get_user_id)
    create_at = Column('create_at', DateTime, nullable=True, default=datetime.datetime.now)
    id_update = Column('id_update', Integer, nullable=True, onupdate=get_user_id)
    update_at = Column('update_at', DateTime, nullable=True, onupdate=datetime.datetime.now)
    placestags = relationship("Placestags",backref='tags')


class Users(base):
    __tablename__ = 'users'

    id_users = Column('id_users', Integer, primary_key=True,autoincrement=True)
    name = Column('name', String(100), nullable=False)
    email = Column('email', String(100), nullable=False, unique=True)
    password = Column('password', String(100), nullable=False)
    is_admin = Column('is_admin', Boolean, default=0, index=True)
    is_active = Column('is_active', Boolean, default=0, index=True)
    id_create = Column('id_create', Integer, nullable=True, default=get_user_id)
    create_at = Column('create_at', DateTime, nullable=True, default=datetime.datetime.now)
    id_update = Column('id_update', Integer, nullable=True, onupdate=get_user_id)
    update_at = Column('update_at', DateTime, nullable=True, onupdate=datetime.datetime.now)
    Index("idx_user_pass", email, password, is_active)
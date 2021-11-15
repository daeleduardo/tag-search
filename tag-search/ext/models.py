import os

from sqlalchemy.sql.sqltypes import DECIMAL, BigInteger
from .constants import env , regex_pattern
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.schema import Index, UniqueConstraint, ForeignKey
from sqlalchemy import Column, String, Integer, Boolean, DateTime, Index, Date,create_engine


db_string = os.getenv("DB_PROD_URI") if os.getenv("FLASK_ENV") == env.PRODUCTION else os.getenv("DB_TEST_URI")
engine = create_engine(db_string, echo=True, echo_pool='debug')
base = declarative_base()
Session = sessionmaker(bind=engine,autocommit=False,autoflush=False)

def set_user_session(session,id):
    if isinstance(id,int):
        return session.execute("set users.id to '"+str(id)+"';")
    raise TypeError("set_user_session: id must be an integer")
    


class Placestags(base):
    __tablename__ = 'places_tags'

    id_place_tag = Column('id_places_tags', Integer, primary_key=True,autoincrement=True)
    id_tag = Column('id_tags', Integer, ForeignKey('tags.id_tags'), index=True)
    id_place = Column('id_places', Integer, ForeignKey('places.id_places'), index=True)
    id_create = Column('id_create', Integer, nullable=True)
    create_at = Column('create_at', DateTime, nullable=True)
    id_update = Column('id_update', Integer, nullable=True)
    update_at = Column('update_at', DateTime, nullable=True)
    Index("idx_place_tag", id_tag, id_place)
    UniqueConstraint('id_tags', 'id_places', name='places_tags')


class Places(base):
    __tablename__ = 'places'

    id_places = Column('id_places', Integer, primary_key=True,autoincrement=True)
    name = Column('name', String(100), nullable=False)
    description = Column('description', String(255), nullable=True)
    phone = Column('phone', String(100), nullable=False, index=True)
    address = Column('address', String(100), nullable=False)
    latitude = Column('latitude', DECIMAL(precision=18,scale=15), nullable=False)
    longitude = Column('longitude', DECIMAL(precision=18,scale=15), nullable=False)
    id_create = Column('id_create', Integer, nullable=True)
    create_at = Column('create_at', DateTime, nullable=True)
    id_update = Column('id_update', Integer, nullable=True)
    update_at = Column('update_at', DateTime, nullable=True)
    Index("idx_phone_place",phone)
    Index("idx_info_place", name, phone,address,unique=True)
    placestags = relationship("Placestags",backref='places')


class Tags(base):
    __tablename__ = 'tags'

    id_tags = Column('id_tags', Integer, primary_key=True,autoincrement=True)
    name = Column('name', String(100), nullable=False, unique=True)
    hash_name = Column('hash_name', BigInteger, nullable=False, index=True)
    id_create = Column('id_create', Integer, nullable=True)
    create_at = Column('create_at', DateTime, nullable=True)
    id_update = Column('id_update', Integer, nullable=True)
    update_at = Column('update_at', DateTime, nullable=True)
    placestags = relationship("Placestags",backref='tags')


class Users(base):
    __tablename__ = 'users'

    id_users = Column('id_users', Integer, primary_key=True,autoincrement=True)
    name = Column('name', String(100), nullable=False)
    email = Column('email', String(100), nullable=False, unique=True)
    password = Column('password', String(100), nullable=False)
    is_admin = Column('is_admin', Boolean, default=0, index=True)
    is_active = Column('is_active', Boolean, default=0, index=True)
    id_create = Column('id_create', Integer, nullable=True)
    create_at = Column('create_at', DateTime, nullable=True)
    id_update = Column('id_update', Integer, nullable=True)
    update_at = Column('update_at', DateTime, nullable=True)
    Index("idx_user_pass", email, password, is_active)
import os

from sqlalchemy.sql.sqltypes import BigInteger
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
    session.execute("set users.id to '"+str(id)+"';")



class Contactstags(base):
    __tablename__ = 'ts_contacts_tags'

    id_contact_tag = Column('id_contacts_tags', Integer, primary_key=True,autoincrement=True)
    id_tag = Column('id_tags', Integer, ForeignKey('ts_tags.id_tags'), index=True)
    id_contact = Column('id_contacts', Integer, ForeignKey('ts_contacts.id_contacts'), index=True)
    id_create = Column('id_create', Integer, nullable=True)
    create_at = Column('create_at', DateTime, nullable=True)
    id_update = Column('id_update', Integer, nullable=True)
    update_at = Column('update_at', DateTime, nullable=True)
    Index("idx_contact_tag", id_tag, id_contact)
    UniqueConstraint('id_tags', 'id_contacts', name='contacts_tags')


class Contacts(base):
    __tablename__ = 'ts_contacts'

    id_contacts = Column('id_contacts', Integer, primary_key=True,autoincrement=True)
    name = Column('name', String(100), nullable=False)
    description = Column('description', String(255), nullable=True)
    phone = Column('phone', String(100), nullable=False, index=True)
    address = Column('address', String(100), nullable=False)
    id_create = Column('id_create', Integer, nullable=True)
    create_at = Column('create_at', DateTime, nullable=True)
    id_update = Column('id_update', Integer, nullable=True)
    update_at = Column('update_at', DateTime, nullable=True)
    Index("idx_phone_contact",phone)
    Index("idx_info_contact", name, phone,address,unique=True)
    contactstags = relationship("Contactstags",backref='ts_contacts')


class Tag(base):
    __tablename__ = 'ts_tags'

    id_tags = Column('id_tags', Integer, primary_key=True,autoincrement=True)
    name = Column('name', String(100), nullable=False, unique=True)
    hash_name = Column('hash_name', BigInteger, nullable=False, index=True)
    id_create = Column('id_create', Integer, nullable=True)
    create_at = Column('create_at', DateTime, nullable=True)
    id_update = Column('id_update', Integer, nullable=True)
    update_at = Column('update_at', DateTime, nullable=True)
    contactstags = relationship("Contactstags",backref='ts_tags')


class User(base):
    __tablename__ = 'ts_users'

    id_users = Column('id_users', Integer, primary_key=True,autoincrement=True)
    name = Column('name', String(100), nullable=False)
    nick = Column('nick', String(100), nullable=False)
    password = Column('password', String(40), nullable=False)
    is_admin = Column('is_admin', Boolean, default=0, index=True)
    id_create = Column('id_create', Integer, nullable=True)
    create_at = Column('create_at', DateTime, nullable=True)
    id_update = Column('id_update', Integer, nullable=True)
    update_at = Column('update_at', DateTime, nullable=True)
    Index("idx_user_pass", name, password)




class Message(base):
    __tablename__ = 'ts_messages'

    id_messages = Column('id_messages', Integer, primary_key=True,autoincrement=True)
    title = Column('title', String(100), nullable=False)
    description = Column('description', String(255), nullable=False)
    expire_date = Column('expire_date', Date, nullable=True, index=True)
    id_create = Column('id_create', Integer, nullable=True)
    create_at = Column('create_at', DateTime, nullable=True)
    id_update = Column('id_update', Integer, nullable=True)
    update_at = Column('update_at', DateTime, nullable=True)


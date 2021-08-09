import json,re
from sqlalchemy.sql import text
from sqlalchemy.sql.expression import update
from ...ext.redis import db_cache
from ...ext.constants import regex_pattern
from ...ext.utils import utils
from ...ext.models import Contactstags, Contacts, Tag, set_user_session
from redis import DataError

class Contact():

    @staticmethod
    def get_contact_by_id(session,id):

        key = 'ts_contact_' + str(id)

        if db_cache.conn().exists(key):

            query = json.loads(db_cache.conn().get(key))

        else:
            sql = text("""
            SELECT  c.id_contacts,
                    c.name,
                    c.phone,
                    c.description,                
                    c.address,
                    array_agg(DISTINCT t.name) AS tags
            FROM ts_contacts c
            LEFT JOIN ts_contacts_tags ct ON c.id_contacts = ct.id_contacts
            LEFT JOIN ts_tags t ON ct.id_tags = t.id_tags
            WHERE c.id_contacts = :id_contacts
            GROUP BY c.id_contacts
            ORDER BY count(1) DESC;
            """)

            query = session.execute(sql, {'id_contacts': id}).first()

        return {"key":key, "query":query}


    @staticmethod
    def get_contact_by_tags(session,tags):


        hash_tags = "0"
        tags = list(tags.split(","))
        for tag in tags:
            if not re.search(regex_pattern.NON_WORDS, tag):
                hash_tag = utils.get_hash(tag)
                hash_tags = str(hash_tags) + "," + str(hash_tag)

        key = 'ts_contact_' + utils.get_hash(str(hash_tags),only_numeric=False)

        if db_cache.conn().exists(key):
            query = json.loads(db_cache.conn().get(key))
        else:
            sql = text("""
            SELECT  c.id_contacts,
                    c.name,
                    c.phone,
                    c.description,                
                    c.address,
                    array_agg(DISTINCT t.name) AS tags
            FROM ts_contacts c
            INNER JOIN ts_contacts_tags ct ON c.id_contacts = ct.id_contacts
            INNER JOIN ts_tags t ON ct.id_tags = t.id_tags
            WHERE t.hash_name  in ("""+ hash_tags +""")
            GROUP BY c.id_contacts
            ORDER BY count(1) DESC;            
            """)
            query = session.execute(sql, {'id_contacts': id}).all()

        return {"key":key, "query":query}

    @staticmethod
    def get_contact_all(session):

        key = 'ts_contact_0'

        if db_cache.conn().exists(key):
            query = json.loads(db_cache.conn().get(key))
        else:        
            sql = text("""
            SELECT  c.id_contacts,
                    c.name,
                    c.description,
                    c.phone,
                    c.address,
                    array_agg(DISTINCT t.name) AS tags
            FROM ts_contacts c
            LEFT JOIN ts_contacts_tags ct ON c.id_contacts = ct.id_contacts
            LEFT JOIN ts_tags t ON ct.id_tags = t.id_tags
            GROUP BY c.id_contacts
            ORDER BY count(1) DESC;            
            """)
            query = session.execute(sql).all()

        return {"key":key, "query":query}

    @staticmethod
    def delete(session,id):

        tags = session.query(Contactstags).filter(
            Contactstags.id_contact == id).all()
        contact = session.query(Contacts).filter(
            Contacts.id_contacts == id).first()

        for tag in tags:
            session.delete(tag)
        session.delete(contact)
        session.commit()

        keys = ['ts_contact_' + str(id), 'ts_contact_0']
        db_cache.delete_many_keys(keys)

        return True

    @staticmethod
    def insert(session,data,id):
        session.begin()
        set_user_session(session,1)
        count = session.query(Contacts).filter(
            Contacts.name == data['name'], Contacts.phone == data['phone'], Contacts.address == data['address']).count()
        if (count != 0):
            raise DataError(
                'Error to add contact, the contact already exists', 400)

        hash_tags = "0"
        for tag in data['tags']:
            if not re.search(regex_pattern.NON_WORDS, tag):
                hash_tag = utils.get_hash(tag)
                t = Tag(name=tag, hash_name=hash_tag)
                hash_tags = str(hash_tags) + "," + str(hash_tag)
                count = session.query(Tag).filter(
                    Tag.hash_name == hash_tag).count()
                if (count == 0):
                    session.add(t)

        contact = Contacts(
            name=data['name'], phone=data['phone'], address=data['address'], description=data['description'])

        session.add(contact)

        session.commit()
        session.begin()

        set_user_session(session,1)

        id_contacts = str("""
            (
                SELECT id_contacts from ts_contacts where
                name='"""+data['name']+"""' and
                phone='"""+data['phone']+"""' and
                address='"""+data['address']+"""'
            )
        """)
        sql = text("""
            INSERT INTO ts_contacts_tags (id_contacts,id_tags) SELECT """+id_contacts+""",id_tags FROM ts_tags where hash_name in (""" + hash_tags + """)
        """)

        session.execute(sql)
        session.commit()

    @staticmethod
    def update(session,data,id_user):
        session.begin()

        set_user_session(session,id_user)

        contact = update(Contacts).where(Contacts.id_contacts == data['id'])
        contact = contact.values(
            name=data['name'], phone=data['phone'], address=data['address'], description=data['description'])
        session.execute(contact)


        tags = session.query(Contactstags).join(Tag, Tag.id_tags == Contactstags.id_tag).filter(
            Contactstags.id_contact == data['id']).all()


        list_tags = data['tags']
        for tag in tags:
            if tag.ts_tags.name in data['tags']:
                list_tags.remove(tag.ts_tags.name)
            else:
                session.delete(tag)

        hash_tags = []
        for tag in list_tags:
            if not re.search(regex_pattern.NON_WORDS, tag):
                hash_tag = utils.get_hash(tag)
                t = Tag(name=tag, hash_name=hash_tag)
                hash_tags.append(hash_tag)
                count = session.query(Tag).filter(
                    Tag.hash_name == hash_tag).count()
                if (count == 0):
                    session.add(t)

        if len(hash_tags) !=0:
            sql = text("""
                INSERT INTO ts_contacts_tags (id_contacts,id_tags) SELECT """+str(data['id'])+""",id_tags FROM ts_tags where hash_name in ('""" + '\',\''.join(hash_tags) + """')
            """)
            session.execute(sql)

        session.commit()
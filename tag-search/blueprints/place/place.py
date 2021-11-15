import re

from sqlalchemy.exc import DataError, DatabaseError
from sqlalchemy.orm import session
from sqlalchemy.sql import text
from sqlalchemy.sql.expression import update
from flask import g
from ..tag.Tag import Tag
from ...ext.redis import db_cache
from ...ext.constants import regex_pattern, cache_time
from ...ext.utils import utils
from ...ext.models import Placestags, Places, Tags, set_user_session, Session



class Place():

    @staticmethod
    def get_place_by_id(id):

        if not isinstance(id, int):
            raise DatabaseError('Error to get place, invalid id. ', 400)

        session = Session()

        sql = text("""
        SELECT  p.id_places,
                p.name,
                p.phone,
                p.description,                
                p.address,
                p.latitude,
                p.longitude,
                array_agg(DISTINCT t.name) AS tags
        FROM places p
        LEFT JOIN places_tags pt ON p.id_places = pt.id_places
        LEFT JOIN tags t ON pt.id_tags = t.id_tags
        WHERE p.id_places = :id_places
        GROUP BY p.id_places
        ORDER BY count(1) DESC;
        """)

        return session.execute(sql, {'id_places': id}).first()

    @staticmethod
    def get_place_by_tags(tags):

        if Tag.is_invalid_tags(tags):
            raise DatabaseError('Error to get place, invalid tags. ', 400)

        session = Session()

        hash_tags = "0"
        for tag in list(tags.split(",")):
            hash_tag = utils.get_hash(tag)
            hash_tags = str(hash_tags) + "," + str(hash_tag)

        sql = text("""
        SELECT  p.id_places,
                p.name,
                p.phone,
                p.description,                
                p.address,
                p.latitude,
                p.longitude,
                array_agg(DISTINCT t.name) AS tags
        FROM places p
        INNER JOIN places_tags pt ON p.id_places = pt.id_places
        INNER JOIN tags t ON pt.id_tags = t.id_tags
        WHERE t.hash_name  in (""" + hash_tags + """)
        GROUP BY p.id_places
        ORDER BY count(1) DESC;            
        """)

        return session.execute(sql).all()

    @staticmethod
    def get_place_all():

        session = Session()

        sql = text("""
        SELECT  p.id_places as id,
                p.name,
                p.latitude,
                p.longitude,
                array_agg(DISTINCT t.name) AS tags
        FROM places p
        INNER JOIN places_tags pt ON p.id_places = pt.id_places
        INNER JOIN tags t ON pt.id_tags = t.id_tags
        GROUP BY p.id_places;
        """)




        return session.execute(sql).all()

    @staticmethod
    def delete(id):

        if g.token['id'] is None:
            raise DatabaseError('Error to delete place, user not found. ', 400)

        try:

            session = Session()
            session.begin()
            place_tags = session.query(Placestags).filter(
                Placestags.id_place == id).all()
            place = session.query(Places).filter(
                Places.id_places == id).first()

            ids_tags = "0"
            for tag in place_tags:
                ids_tags = str(ids_tags) + "," + str(tag.id_tag)
                session.delete(tag)
                session.flush()

            session.delete(place)
            session.commit()

            session.begin()
            sql = text("""
                DELETE
                FROM tags
                WHERE id_tags in (
                    SELECT t.id_tags
                    FROM tags t
                    LEFT JOIN places_tags pt ON t.id_tags = pt.id_tags 
                    WHERE pt.id_tags in (""" + ids_tags + """)
                        AND pt.id_tags IS NULL
                )
            """)
            session.execute(sql)
            session.commit()

            return True
        except DatabaseError as e:
            if session is not None:
                session.rollback()
            raise DatabaseError(
                'Error to delete place ' + str(e.args[0]), 400)
        finally:
            session.close()

    @staticmethod
    def check_if_place_exists(data):
        session = Session()
        count = session.query(Places).filter(
            Places.name == data['name'], Places.phone == data['phone'], Places.address == data['address']).count()
        session.close()
        return (int(count) > 0)

    @staticmethod
    def is_valid_lat_lng(lat, lng):
        lat = str(lat)
        lng = str(lng)
        valid_lat = re.match(regex_pattern.LAT_LNG, lat)
        valid_lng = re.match(regex_pattern.LAT_LNG, lng)
        return valid_lat and valid_lng and len(lat) < 20 and len(lng) < 20

    @staticmethod
    def insert(data):

        try:
            if g.token['id'] is None:
                raise DatabaseError(
                    'Error to add place, user not found.', 400)

            if Tag.is_invalid_tags(data['tags']):
                raise DatabaseError('Error to add place, invalid tags. ', 400)

            if (Place.check_if_place_exists(data)):
                raise DataError(
                    'Error to add place, the place already exists', 400)

            if (not Place.is_valid_lat_lng(data['latitude'], data['longitude'])):
                raise DataError(
                    'Error to add place, invalid latitude and longitude', 400)

            session = Session()
            session.begin()
            set_user_session(session, g.token['id'])
            hash_tags = "0"
            
            for tag in data['tags']:
                hash_tag = utils.get_hash(tag)
                t = Tags(name=tag, hash_name=hash_tag)
                hash_tags = str(hash_tags) + "," + str(hash_tag)
                count = session.query(Tags).filter(
                    Tags.hash_name == hash_tag).count()
                if (count == 0):
                    session.add(t)
                    session.flush()

            session.commit()
            session.begin()

            place = Places(
                name=str(data['name']).strip(),
                phone=str(data['phone']).strip(),
                address=str(data['address']).strip(),
                description=str(data['description']).strip(),
                latitude=data['latitude'],
                longitude=data['longitude'])

            session.add(place)

            session.commit()
            session.begin()

            set_user_session(session, g.token['id'])

            id_places = str("""
                (
                    SELECT id_places from places where
                    name='"""+data['name']+"""' and
                    phone='"""+data['phone']+"""' and
                    address='"""+data['address']+"""'
                )
            """)
            sql = text("""
                INSERT INTO places_tags (id_places,id_tags) 
                SELECT """+id_places+""",id_tags FROM tags 
                WHERE hash_name in (""" + hash_tags + """)
            """)

            session.execute(sql)
            session.commit()

            return True
        except DatabaseError as e:
            if session is not None:
                session.rollback()
            raise DatabaseError(
                'Error to insert place ' + str(e.args[0]), 400)
        except AttributeError as e:
            if session is not None:
                session.rollback()
            raise AttributeError(
                'Error to add place, user not found.', 400)
        except TypeError as e:
            if session is not None:
                session.rollback()
            raise TypeError(
                'Error to add place, some field are unfilled or incorrect. ', 400)
        finally:
            session.close()

    @staticmethod
    def update(data):

        try:
            session = Session()

            if g.token['id'] is None:
                raise DatabaseError(
                    'Error to update place, user not found. ', 400)

            if Tag.is_invalid_tags(data['tags']):
                raise DatabaseError(
                    'Error to update place, invalid tags. ', 400)

            if (not Place.is_valid_lat_lng(data['latitude'], data['longitude'])):
                raise DataError(
                    'Error to add place, invalid latitude and longitude', 400)

            session.begin()
            set_user_session(session, g.token['id'])

            place = update(Places).where(Places.id_places == data['id'])
            place = place.values(
                name=data['name'],
                phone=data['phone'],
                address=data['address'],
                description=data['description'],
                latitude=data['latitude'],
                longitude=data['longitude'])

            session.execute(place)

            session.commit()
            session.begin()

            tags = session.query(Placestags).join(Tags, Tags.id_tags == Placestags.id_tag).filter(
                Placestags.id_place == data['id']).all()

            list_tags = data['tags']
            for tag in tags:
                if tag.tags.name in data['tags']:
                    list_tags.remove(tag.tags.name)
                else:
                    session.delete(tag)
                    session.flush()

            hash_tags = []
            for tag in list_tags:
                hash_tag = utils.get_hash(tag)
                t = Tags(name=tag, hash_name=hash_tag)
                hash_tags.append(hash_tag)
                count = session.query(Tags).filter(
                    Tags.hash_name == hash_tag).count()
                if (count == 0):
                    session.add(t)
                    session.flush()

            if len(hash_tags) != 0:
                sql = text("""
                    INSERT INTO places_tags (id_places,id_tags) 
                    SELECT """+str(data['id'])+""",id_tags 
                    FROM tags where hash_name in ('""" + '\',\''.join(hash_tags) + """')
                """)
                session.execute(sql)

            session.commit()

        except DatabaseError as e:
            if session is not None:
                session.rollback()
            raise DatabaseError(
                'Error to insert place ' + str(e.args[0]), 400)
        except AttributeError as e:
            if session is not None:
                session.rollback()
            raise AttributeError(
                'Error to add place, user not found.', 400)
        except TypeError as e:
            if session is not None:
                session.rollback()
            raise TypeError(
                'Error to add place, some field are unfilled or incorrect. ', 400)
        finally:
            if session is not None:
                session.close()

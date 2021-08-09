import hashlib
import json

from sqlalchemy.util.langhelpers import NoneType


class utils():

    @staticmethod
    def add_key_value_dict(key, value, dictionary): return (
        value is not None) and dictionary.update({key: value})

    @staticmethod
    def get_value_if_exists_dict(key, dict):
        if (key in dict.keys()):
            return dict[key]
        return None

    @staticmethod
    def get_hash(txt_to_hash, only_numeric=True):

        txt = str(txt_to_hash).strip().encode('utf-8')

        if(txt is None or txt == ''):
            raise TypeError('Texto informado incorreto', 400)

        sha_hash = hashlib.sha256(txt).hexdigest()
        md5_hash = hashlib.md5(txt).hexdigest()
        
        if (only_numeric):
            sha_hash = int(sha_hash, 16) % 10**9
            md5_hash = int(md5_hash, 16) % 10**9

        return str(sha_hash) + str(md5_hash)

    @staticmethod
    def row2dict(row):
        d = {}
        if row is None or row is NoneType:
            return d
        elif hasattr(row, '__table__'):
            for column in row.__table__.columns:
                d[column.name] = str(getattr(row, column.name))
        elif hasattr(row, '_fields'):
            d = row._asdict()
        else:
            for column in row.keys():
                d[column] = str(row[column])
        return d

    @staticmethod
    def result2dict(query):
        result = []
        if query is NoneType or isinstance(query, NoneType):
            return result
        if hasattr(query, '_asdict'):
            result.append(query._asdict())
        elif hasattr(query, '__len__'):
            for row in query:
                result.append(utils.row2dict(row))
        else:
            result.append(utils.row2dict(query))
        return result

    @staticmethod
    def dict2str(dict):
        return str(json.dumps(dict, separators=(',', ':')))


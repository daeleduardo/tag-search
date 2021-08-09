from logging import setLogRecordFactory
import os
import redis


class db_cache():
    @staticmethod
    def conn():
        return redis.Redis(
            host=os.getenv('CACHE_HOST'),
            port=os.getenv('CACHE_PORT'),
            password=os.getenv('CACHE_PASS'))

    @staticmethod
    def delete_many_keys(keys):
        redis_conn = db_cache.conn()
        for key in keys:
            redis_conn.delete(key)

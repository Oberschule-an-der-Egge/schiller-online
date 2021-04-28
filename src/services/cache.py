"""
Redis zur User Session Verwaltung

Mehr Details zu Redis und der Implementierung in Schiller-Online unter docs/redis.md
"""

import json
import os
import time
import redis
from flask import session

from src.config import production


class RedisConnection:
    """Singleton, der immer die gleiche Connection zurückgibt
    DB connections müssen nicht gemanaged werden, jede Instanz von Redis hat ihren eigenen Connection Pool und
    managed die Verbindungen selbst. Das bedeutet allerdings, das pro User Session nur eine Instanz aufgemacht
    werden sollte.
    https://stackoverflow.com/questions/57902876/how-to-use-connection-pooling-for-redis-strictredis
    https://pypi.org/project/redis/#connection-pools
    """
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            redis_conf = {
                'host': 'localhost',
                'port': 6379,
                'db': 0,
                'decode_responses': True,
            }
            # current_app is not available yet on import
            if os.getenv('FLASK_ENV') != 'development':
                redis_socket = production.REDIS_SOCKET
                redis_pass = production.REDIS_PASS
            else:
                redis_socket = None
                redis_pass = None
            # pool = redis.ConnectionPool(**redis_conf)
            cls.instance = redis.StrictRedis(unix_socket_path=redis_socket, password=redis_pass, decode_responses=True)
        return cls.instance


def write(key=None, value=None, hash=None, mapping: dict = None):
    _r = RedisConnection()
    if hash:
        full_hash = "{}:{}".format(hash, session['token'])
        if mapping:
            _r.hset(full_hash, mapping=mapping)
        else:
            _r.hset(full_hash, key, value)

    else:
        # is Redis SET
        full_key = "{}:{}".format(key, session['token'])
        _r.sadd(full_key, value)


def read(key=None, hash: str = None):
    _r = RedisConnection()
    if hash:
        full_hash = "{}:{}".format(hash, session['token'])
        return _r.hget(full_hash, key)

    else:
        # is Redis SET
        full_key = "{}:{}".format(key, session['token'])
        return _r.smembers(full_key)


def delete(key, member=None, hash: str = None):
    _r = RedisConnection()
    if hash:
        full_hash = "{}:{}".format(hash, session['token'])
        _r.hdel(full_hash, key)

    else:
        # is Redis SET
        full_key = "{}:{}".format(key, session['token'])
        _r.srem(full_key, member)


def hash_exists(name):
    """Existiert das HASH in Redis?
    """
    _r = RedisConnection()
    if _r.hkeys(name + ':' + session['token']):
        return True
    else:
        return False


def set_exists(name):
    """Existiert das SET in Redis?
    """
    _r = RedisConnection()
    if _r.smembers(name + ':' + session['token']):
        return True
    else:
        return False


def read_static_set(key):
    _r = RedisConnection()
    return _r.smembers(key)


def read_static_hash(key, hash: str = None):
    _r = RedisConnection()
    return _r.hget(hash, key)


def serialize(key, input_dict: dict = None):
    _r = RedisConnection()
    input_dict_serialized = json.dumps(input_dict)
    full_key = "{}:{}".format(key, session['token'])
    _r.set(full_key, input_dict_serialized)


def deserialize(key):
    _r = RedisConnection()
    full_key = "{}:{}".format(key, session['token'])
    dict_serialized = _r.get(full_key)
    return json.loads(dict_serialized)


def add_timestamp():
    """User mit Timestamp in SORTEDSET speichern
    """
    _r = RedisConnection()
    # time.time() instead of datetime.utcnow() for sorting
    timestamp = time.time()
    token = session['token']
    _r.zadd('recent:', {token: timestamp})

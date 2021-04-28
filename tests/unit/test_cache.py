
from src.services import cache


def test_read_write_hash(client):
    client.get('/')
    r = cache.RedisConnection()
    r.hset('testkey', 'testval', 'testwat')
    cache.write(key='my_key', value='my_value', hash='session')
    result = cache.read(key='my_key', hash='session')
    assert result == 'my_value'


def test_read_write_set(client):
    client.get('/')
    cache.write(key='my_key', value='my_value')
    result = cache.read(key='my_key')
    assert result == {'my_value'}


def test_delete_hash_or_set(client):
    client.get('/')
    cache.write(key='my_key', value='my_value', hash='session')
    result = cache.read(key='my_key', hash='session')
    assert result == 'my_value'
    cache.delete(key='my_key', hash='session')
    result = cache.read(key='my_key', hash='session')
    assert result is None

    cache.write(key='my_key', value='my_value')
    result = cache.read(key='my_key')
    assert result == {'my_value'}
    cache.delete(key='my_key', member='my_value')
    result = cache.read(key='my_key')
    assert result == set()

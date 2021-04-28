from uuid import UUID

from flask import session

from src import config
from src.services import cache


def test_routes_nonsense(client):
    rv = client.get('/nudge-nudge')
    assert rv.status_code == 404


def test_routes_index(client):
    rv = client.get('/')
    assert rv.status_code == 200
    assert b'Guten Tag und Herzlich Willkommen' in rv.data


def test_routes_index_sets_session(client):
    rv = client.get('/')
    token = session['token']
    assert UUID(token, version=4)


def test_routes_index_sets_timestamp(client):
    rv = client.get('/')
    r = cache.RedisConnection()
    result = r.zrange('recent:', 0, 0, withscores=True)
    assert len(result[0]) == 2  # [(token, time)]


def test_routes_redirect_rushing(client):
    rv = client.get('/2', follow_redirects=True)
    assert b'Fehler: Cookies m\xc3\xbcssen aktiviert sein.' in rv.data
    # rv = client.get('/3', follow_redirects=True)
    # assert b'Fehler: Cookies m\xc3\xbcssen aktiviert sein.' in rv.data
    # rv = client.get('/4', follow_redirects=True)
    # assert b'Fehler: Cookies m\xc3\xbcssen aktiviert sein.' in rv.data
    # rv = client.get('/5', follow_redirects=True)
    # assert b'Fehler: Cookies m\xc3\xbcssen aktiviert sein.' in rv.data
    # rv = client.get('/6', follow_redirects=True)
    # assert b'Fehler: Cookies m\xc3\xbcssen aktiviert sein.' in rv.data
    rv = client.get('/')
    assert rv.status_code == 200
    rv = client.get('/2', follow_redirects=True)
    assert b'Bitte bei Schritt 1 beginnen.' in rv.data
    rv = client.get('/3', follow_redirects=True)
    assert b'Bitte bei Schritt 1 beginnen.' in rv.data
    rv = client.get('/4', follow_redirects=True)
    assert b'Bitte bei Schritt 1 beginnen.' in rv.data
    rv = client.get('/5', follow_redirects=True)
    assert b'Bitte bei Schritt 1 beginnen.' in rv.data
    rv = client.get('/6', follow_redirects=True)
    assert b'Bitte bei Schritt 1 beginnen.' in rv.data
    rv = client.get('/output', follow_redirects=True)
    assert b'Bitte bei Schritt 1 beginnen.' in rv.data


def test_routes_session_empty(client):
    rv = client.get('/session')
    assert rv.status_code == 200
    assert rv.data == b'{}\n'


def test_routes_session(client):
    rv = client.get('/')
    rv = client.get('/session')
    assert rv.status_code == 200
    assert b'token' in rv.data


def test_routes_redis(client):
    rv = client.get('/')
    rv = client.get('/redis')
    assert rv.status_code == 200
    assert b'{"possiblepruefung":[],"pruefungsfaecher":[],"session":{},"stundensumme":{},' in rv.data
    assert b'"you_may_call_me_raster":{"e11":{},"e12":{},"q11":{},"q12":{},"q21":{},"q22"' in rv.data



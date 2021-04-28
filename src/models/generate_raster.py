"""
Raster für die finale Darstellung als PDF / XLSX

Das "raster" hat die Struktur eines Python dict() / JSON, ist aber in Redis in mehrere HASH aufgeteilt.
Eine grafische Darstellung findet sich in docs/redis.md.
Dazu kommt ein weiterer HASH "session", mit den Daten der Usersession,
sowie zwei SET "pruefungsfaecher" und "possiblepruefung" zur Festlegung der Prüfungsfächer.
"""

from flask import session
from src.services import cache

# Redis access for module generate_raster
r = cache.RedisConnection()


def generate_raster():
    token = session['token']

    def hash_name(halbjahr):
        return "{}:{}".format(halbjahr, token)

    profilbuchstabe = r.hget('session:' + token, 'profilbuchstabe')
    freierlk = r.hget('session:' + token, 'freierlk')

    with r.pipeline() as pipe:
        for h in ['e11', 'e12']:
            pipe.hset(hash_name(h), mapping={
                'deu': 4,
                'eng': 4,
                'mat': 4,
                'pae': 3,
                'ges': 2,
                'pol': 2,
                'spx': 2,
                'met': 2,
                'slz': 2,
            })

        for h in ['q11', 'q12', 'q21', 'q22']:
            pipe.hset(hash_name(h), mapping={
                'deu': 3,
                'eng': 3,
                'mat': 3,
                'spx': 2,
            })

        for h in ['q11', 'q12']:
            pipe.hset(hash_name(h), mapping={
                'rel': 2,
                'slz': 2,
                'prj': 2,
            })

        # Werte für Profile anpassen

        if profilbuchstabe == 'A':
            for h in ['q11', 'q12', 'q21', 'q22']:
                pipe.hset(hash_name(h), mapping={
                    'deu': 5,
                    'kun': 3,
                    'ges': 3,
                })

        elif profilbuchstabe == 'B':
            for h in ['q11', 'q12', 'q21', 'q22']:
                pipe.hset(hash_name(h), mapping={
                    'eng': 5,
                    'ges': 3,
                    'bio': 3,
                })

        elif profilbuchstabe == 'C':
            for h in ['q11', 'q12', 'q21', 'q22']:
                pipe.hset(hash_name(h), mapping={
                    'pae': 5,
                    'pol': 3,
                    'bio': 3,
                })

        elif profilbuchstabe == 'D':
            for h in ['q11', 'q12', 'q21', 'q22']:
                pipe.hset(hash_name(h), mapping={
                    'bio': 5,
                    'che': 3,
                    'pol': 3,
                })

        elif profilbuchstabe == 'E':
            for h in ['q11', 'q12', 'q21', 'q22']:
                pipe.hset(hash_name(h), mapping={
                    'pae': 3,
                    'bio': 3,
                    'sth': 2,
                })
            for h in ['e12']:
                pipe.hset(hash_name(h), 'sth', 3)
            for h in ['q11', 'q12']:
                pipe.hset(hash_name(h), 'spx', 4)
            for h in ['q21', 'q22']:
                pipe.hset(hash_name(h), 'spx', 2)

        # Werte für freie LKs anpassen
        for h in ['q11', 'q12', 'q21', 'q22']:
            pipe.hset(hash_name(h), freierlk, 5)

        pipe.execute()


def generate_possiblepruefung():
    token = session['token']
    possiblepruefung = 'possiblepruefung:' + token
    profilbuchstabe = r.hget('session:' + token, 'profilbuchstabe')

    with r.pipeline() as pipe:

        # Kernfächer als mögliche Prüfungsfächer
        # Redundanz für bessere Übersicht in Kauf genommen.
        pipe.sadd(possiblepruefung, 'deu')
        pipe.sadd(possiblepruefung, 'eng')
        pipe.sadd(possiblepruefung, 'mat')

        if profilbuchstabe == 'A':
            pipe.sadd(possiblepruefung, 'deu')
            pipe.sadd(possiblepruefung, 'kun')
            pipe.sadd(possiblepruefung, 'ges')

        if profilbuchstabe == 'B':
            pipe.sadd(possiblepruefung, 'eng')
            pipe.sadd(possiblepruefung, 'ges')
            pipe.sadd(possiblepruefung, 'bio')

        if profilbuchstabe == 'C':
            pipe.sadd(possiblepruefung, 'pae')
            pipe.sadd(possiblepruefung, 'pol')
            pipe.sadd(possiblepruefung, 'bio')

        if profilbuchstabe == 'D':
            pipe.sadd(possiblepruefung, 'bio')
            pipe.sadd(possiblepruefung, 'pol')
            pipe.sadd(possiblepruefung, 'che')

        if profilbuchstabe == 'E':
            pipe.sadd(possiblepruefung, 'sth')
            pipe.sadd(possiblepruefung, 'spx')
            pipe.sadd(possiblepruefung, 'mat')
            pipe.sadd(possiblepruefung, 'pae')
            pipe.sadd(possiblepruefung, 'bio')

        pipe.execute()


def generate_pruefungsfaecher():
    token = session['token']
    pruefungsfaecher = 'pruefungsfaecher:' + token
    profilbuchstabe = r.hget('session:' + token, 'profilbuchstabe')

    with r.pipeline() as pipe:

        if profilbuchstabe == 'A':
            pipe.sadd(pruefungsfaecher, 'deu')

        if profilbuchstabe == 'B':
            pipe.sadd(pruefungsfaecher, 'eng')

        if profilbuchstabe == 'C':
            pipe.sadd(pruefungsfaecher, 'pae')

        if profilbuchstabe == 'D':
            pipe.sadd(pruefungsfaecher, 'bio')

        if profilbuchstabe == 'E':
            pipe.sadd(pruefungsfaecher, 'sth')
            pipe.sadd(pruefungsfaecher, 'spx')
            pipe.sadd(pruefungsfaecher, 'mat')

        pipe.execute()


def generate_freierlk():
    token = session['token']
    possiblepruefung = 'possiblepruefung:' + token
    pruefungsfaecher = 'pruefungsfaecher:' + token
    freierlk = r.hget('session:' + token, 'freierlk')

    def hash_name(halbjahr):
        return "{}:{}".format(halbjahr, token)

    with r.pipeline() as pipe:

        # possibleprüfung wird nie für freierlk gebraucht,
        # Eintragung der Vollständigkeit halber
        pipe.sadd(possiblepruefung, freierlk)
        pipe.sadd(pruefungsfaecher, freierlk)

        for h in ['q11', 'q12', 'q21', 'q22']:
            pipe.hset(hash_name(h), freierlk, 5)

        pipe.execute()

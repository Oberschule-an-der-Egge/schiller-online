"""
Zuordnungs-Tabellen zur Unterstützung des Models in generate_raster.py

- feld_fach : Welche Fächer sind im Aufgabenfeld (z.B. Sport: 'spor')
- fach_feld : Welches Aufgabenfeld (agf) hat ein bestimmtes Fach (z.B. Kunst: 'kun')
- fach_short_long : Zuordnung lange (z.b. 'Darstellendes Spiel') zu kurzer ('dar') Fachbezeichnung
- possiblepruefung_filter_special : Spezieller Filter zum Festlegen der Prüfungsfächer

"""

from src.services import cache


def feld_fach():
    r = cache.RedisConnection()

    with r.pipeline() as pipe:

        for feld in ['agf1', 'agf2', 'agf3', 'oagf', 'spor', 'lern']:

            feld_name = "feld:{}".format(feld)

            if feld == 'agf1':
                for fach in ['deu', 'eng', 'fra', 'lat', 'spa', 'rus', 'tur', 'dar', 'mus', 'kun']:
                    pipe.sadd(feld_name, fach)

            if feld == 'agf2':
                for fach in ['ges', 'pol', 'geo', 'pae', 'psy', 'rel']:
                    pipe.sadd(feld_name, fach)

            if feld == 'agf3':
                for fach in ['mat', 'phy', 'che', 'bio']:
                    pipe.sadd(feld_name, fach)

            if feld == 'oagf':
                pipe.sadd(feld_name, 'inf')

            if feld == 'spor':
                for fach in ['spx', 'sth']:
                    pipe.sadd(feld_name, fach)

            if feld == 'lern':
                for fach in ['met', 'slz', 'prj']:
                    pipe.sadd(feld_name, fach)

        pipe.execute()


def fach_feld():
    r = cache.RedisConnection()

    with r.pipeline() as pipe:

        for fach in ['deu', 'eng', 'fra', 'lat', 'spa', 'rus', 'tur', 'dar', 'mus', 'kun']:
            pipe.hset('fach_feld', fach, 'agf1')

        for fach in ['ges', 'pol', 'geo', 'pae', 'psy', 'rel']:
            pipe.hset('fach_feld', fach, 'agf2')

        for fach in ['mat', 'phy', 'che', 'bio']:
            pipe.hset('fach_feld', fach, 'agf3')

        pipe.hset('fach_feld', 'inf', 'oagf')

        for fach in ['spx', 'sth']:
            pipe.hset('fach_feld', fach, 'spor')

        for fach in ['met', 'slz', 'prj']:
            pipe.hset('fach_feld', fach, 'lern')

        pipe.execute()


def fach_short_long():
    r = cache.RedisConnection()

    with r.pipeline() as pipe:

        pipe.hset('fach_short_long', 'deu', 'Deutsch')
        pipe.hset('fach_short_long', 'eng', 'Englisch')
        pipe.hset('fach_short_long', 'fra', 'Französisch')
        pipe.hset('fach_short_long', 'lat', 'Latein')
        pipe.hset('fach_short_long', 'spa', 'Spanisch')
        pipe.hset('fach_short_long', 'rus', 'Russisch')
        pipe.hset('fach_short_long', 'tur', 'Türkisch')
        pipe.hset('fach_short_long', 'dar', 'Darstellendes Spiel')
        pipe.hset('fach_short_long', 'mus', 'Musik')
        pipe.hset('fach_short_long', 'kun', 'Kunst')

        pipe.hset('fach_short_long', 'ges', 'Geschichte')
        pipe.hset('fach_short_long', 'pol', 'Politik')
        pipe.hset('fach_short_long', 'geo', 'Geographie')
        pipe.hset('fach_short_long', 'pae', 'Pädagogik')
        pipe.hset('fach_short_long', 'psy', 'Psychologie')
        pipe.hset('fach_short_long', 'rel', 'Religion')

        pipe.hset('fach_short_long', 'mat', 'Mathe')
        pipe.hset('fach_short_long', 'phy', 'Physik')
        pipe.hset('fach_short_long', 'che', 'Chemie')
        pipe.hset('fach_short_long', 'bio', 'Biologie')

        pipe.hset('fach_short_long', 'inf', 'Informatik')

        pipe.hset('fach_short_long', 'sth', 'Theorie')
        pipe.hset('fach_short_long', 'spx', 'Praxis')

        pipe.hset('fach_short_long', 'met', 'Methoden')
        pipe.hset('fach_short_long', 'slz', 'Selbstlernzeit')
        pipe.hset('fach_short_long', 'prj', 'Projektstunden')

        pipe.execute()


def possiblepruefung_filter_special():
    """Filter out Sport-Profil (E) Prüfungsfächer
    @routes.py:197 -> possible_diff = r.sdiff(...
    """
    r = cache.RedisConnection()

    r.sadd('e_profil', 'sth', 'spx')

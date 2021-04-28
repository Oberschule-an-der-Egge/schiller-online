from flask import request

from src.services import cache
from src.views.macros import radio


def update_raster(belegt=True):

    if not belegt:
        for h in ['e12', 'q11', 'q12', 'q21', 'q22']:
            cache.delete('inf', hash=h)
    else:
        cache.write('inf', 2, hash='e12')
        for h in ['q11', 'q12', 'q21', 'q22']:
            cache.write('inf', 3, hash=h)


def update_possiblepruefung():
    cache.write('possiblepruefung', 'inf')


def process():

    error = []

    toggleinfo = radio(request, 'info', error)

    if not error:
        cache.write('toggleinfo', str(toggleinfo), hash='session')

    if toggleinfo:
        update_raster(belegt=True)
        # Todo: Noch nicht als Prüfungsfach erlauben.
        # update_possiblepruefung(r)
    else:
        update_raster(belegt=False)

    return error

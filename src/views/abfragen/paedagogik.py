from flask import request

from src.services import cache
from src.views.macros import radio


def update_raster(halbjahre, belegt=True, reset=False):
    if reset or not belegt:
        for h in halbjahre:
            cache.delete('pae', hash=h)
    else:
        for h in halbjahre:
            cache.write('pae', 3, hash=h)


def update_possiblepruefung(reset=False):
    if reset:
        cache.delete('possiblepruefung', 'pae')
    else:
        cache.write('possiblepruefung', 'pae')


def process():

    error = []
    ignore_error = []
    profilbuchstabe = cache.read('profilbuchstabe', hash='session')
    freierlk = cache.read('freierlk', hash='session')

    if profilbuchstabe in ['A', 'B', 'D'] and freierlk != 'pae':

        paeq1 = radio(request, 'paeq1', error)
        paeq2 = radio(request, 'paeq2', ignore_error)

        update_raster(['q11', 'q12'], belegt=paeq1)

        if paeq2 is not None:
            update_raster(['q21', 'q22'], belegt=paeq2)
            if paeq2 is True:
                update_possiblepruefung()

    return error


def retry():

    error = []
    ignore_error = []
    profilbuchstabe = cache.read('profilbuchstabe', hash='session')
    freierlk = cache.read('freierlk', hash='session')

    if profilbuchstabe in ['A', 'B', 'D'] and freierlk != 'pae':

        paeq1 = radio(request, 'paeq1', ignore_error)
        paeq2 = radio(request, 'paeq2', ignore_error)

        if paeq1 is not None:
            update_raster(['q11', 'q12', 'q21', 'q22'], reset=True)
            update_possiblepruefung(reset=True)

            update_raster(['q11', 'q12'], belegt=paeq1)

            if paeq2 is not None:
                update_raster(['q21', 'q22'], belegt=paeq2)
                if paeq2 is True:
                    update_possiblepruefung()

    return error

from flask import request

from src.services import cache
from src.views.macros import radio


def update_raster(halbjahre, belegt=True, reset=False):

    stunden = 3

    if reset or not belegt:
        for h in halbjahre:
            cache.delete('psy', hash=h)
    else:
        for h in halbjahre:
            if h in ['e11', 'e12']:
                stunden = 2
            cache.write('psy', stunden, hash=h)


def update_possiblepruefung():
    cache.write('possiblepruefung', 'psy')


def process():

    error = []
    ignore_error = []

    psye1 = radio(request, 'psye1', error)
    psye2 = radio(request, 'psye2', error)
    psyq1 = radio(request, 'psyq1', ignore_error)
    psyq2 = radio(request, 'psyq2', ignore_error)

    update_raster(['e11'], belegt=psye1)
    update_raster(['e12'], belegt=psye2)
    if psyq1 is not None:
        update_raster(['q11', 'q12'], belegt=psyq1)
    if psyq2 is not None:
        update_raster(['q21', 'q22'], belegt=psyq2)
        if psyq2 is True:
            update_possiblepruefung()

    return error


def retry():

    error = []
    ignore_error = []

    psye1 = radio(request, 'psye1', ignore_error)
    psye2 = radio(request, 'psye2', ignore_error)

    if psye1 is not None and psye2 is not None:
        psyq1 = radio(request, 'psyq1', error)
        psyq2 = radio(request, 'psyq2', ignore_error)

        update_raster(['q11', 'q12', 'q21', 'q22'], reset=True)
        update_possiblepruefung()

        if psyq1 is not None:
            update_raster(['q11', 'q12'], belegt=psyq1)
        if psyq2 is not None:
            update_raster(['q21', 'q22'], belegt=psyq2)
            if psyq2 is True:
                update_possiblepruefung()

    return error

from flask import request

from src.services import cache
from src.views.macros import radio


def update_raster(halbjahre, belegt=True, reset=False):

    stunden = 3

    if reset or not belegt:
        for h in halbjahre:
            cache.delete('geo', hash=h)
    else:
        for h in halbjahre:
            if h in ['e11', 'e12']:
                stunden = 2
            cache.write('geo', stunden, hash=h)


def update_possiblepruefung(reset=False):
    if reset:
        cache.delete('possiblepruefung', 'geo')
    else:
        cache.write('possiblepruefung', 'geo')


def process():

    error = []
    ignore_error = []

    geoe1 = radio(request, 'geoe1', error)
    geoe2 = radio(request, 'geoe2', error)
    geoq1 = radio(request, 'geoq1', ignore_error)
    geoq2 = radio(request, 'geoq2', ignore_error)

    update_raster(['e11'], belegt=geoe1)
    update_raster(['e12'], belegt=geoe2)
    if geoq1 is not None:
        update_raster(['q11', 'q12'], belegt=geoq1)
    if geoq2 is not None:
        update_raster(['q21', 'q22'], belegt=geoq2)
        if geoq2 is True:
            update_possiblepruefung()
    return error


def retry():

    error = []
    ignore_error = []

    geoe1 = radio(request, 'geoe1', ignore_error)
    geoe2 = radio(request, 'geoe2', ignore_error)

    if geoe1 is not None and geoe2 is not None:
        geoq1 = radio(request, 'geoq1', error)
        geoq2 = radio(request, 'geoq2', ignore_error)

        update_raster(['q11', 'q12', 'q21', 'q22'], reset=True)
        update_possiblepruefung(reset=True)

        if geoq1 is not None:
            update_raster(['q11', 'q12'], belegt=geoq1)
        if geoq2 is not None:
            update_raster(['q21', 'q22'], belegt=geoq2)
            if geoq2 is True:
                update_possiblepruefung()
    return error

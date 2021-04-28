from flask import request

from src.services import cache
from src.views.macros import select


def update_raster(halbjahre, fach=None, reset=False):

    for h in halbjahre:
        if reset:
            cache.delete(fach, hash=h)
        else:
            if h in ['e11', 'e12']:
                stunden = 2
            else:
                stunden = 3

            cache.write(fach, stunden, hash=h)


def process():

    error = []
    profilbuchstabe = cache.read('profilbuchstabe', hash='session')

    kuenstlerischesfach_e11 = select(request, 'kuenstlerischesfach_e11', error)
    kfach = kuenstlerischesfach_e11

    if not error:
        update_raster(['e11'], fach=kuenstlerischesfach_e11)

    if profilbuchstabe != 'A':
        kuenstlerischesfach_e12 = select(request, 'kuenstlerischesfach_e12', error)
        if not error:
            kfach = kuenstlerischesfach_e12
            update_raster(['e12', 'q11', 'q12'], fach=kuenstlerischesfach_e12)
    else:
        # GenerateRaster füllt Q11-Q22 für A-Profil mit Kunst
        update_raster(['e12'], fach='kun')

    cache.write('kuenstlerischesfach', kfach, hash='session')

    return error

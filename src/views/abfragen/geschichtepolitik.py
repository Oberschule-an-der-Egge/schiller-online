from flask import request

from src.services import cache
from src.views.macros import radio


def update_raster(halbjahre, fach=None, belegt=True, reset=False):

    if reset or not belegt:
        for h in halbjahre:
            cache.delete(fach, hash=h)
    else:
        for h in halbjahre:
            cache.write(fach, 3, hash=h)


def update_possiblepruefung():

    if cache.read('ges', hash='q22'):
        cache.write('possiblepruefung', 'ges')
    else:
        cache.delete('possiblepruefung', 'ges')

    if cache.read('pol', hash='q22'):
        cache.write('possiblepruefung', 'pol')
    else:
        cache.delete('possiblepruefung', 'pol')


def process():

    error = []
    ignore_error = []
    profilbuchstabe = cache.read('profilbuchstabe', hash='session')

    if profilbuchstabe == 'A' or profilbuchstabe == 'B':

        polq1 = radio(request, 'polq1', error)
        polq2 = radio(request, 'polq2', ignore_error)

        update_raster(['q11', 'q12'], fach='pol', belegt=polq1)

        if polq2 is not None:
            update_raster(['q21', 'q22'], fach='pol', belegt=polq2)

    if profilbuchstabe == 'C' or profilbuchstabe == 'D':

        gesq1 = radio(request, 'gesq1', error)
        gesq2 = radio(request, 'gesq2', ignore_error)

        update_raster(['q11', 'q12'], fach='ges', belegt=gesq1)

        if gesq2 is not None:
            update_raster(['q21', 'q22'], fach='ges', belegt=gesq2)

    if profilbuchstabe == 'E':

        polq1 = radio(request, 'polq1', error)
        polq2 = radio(request, 'polq2', ignore_error)
        gesq1 = radio(request, 'gesq1', error)
        gesq2 = radio(request, 'gesq2', ignore_error)

        if polq1 and not polq2:
            msg = "Sie müssen Politik in der Q-Phase durchgängig belegen."
            error.append(msg)
        elif not gesq1 and not polq1:
            msg = "Sie müssen entweder Geschichte in der Q1 oder Politik in der Q1 und Q2 belegen."
            error.append(msg)

        update_raster(['q11', 'q12'], fach='pol', belegt=polq1)
        if polq2 is not None:
            update_raster(['q21', 'q22'], fach='pol', belegt=polq2)

        update_raster(['q11', 'q12'], fach='ges', belegt=gesq1)
        if gesq2 is not None:
            update_raster(['q21', 'q22'], fach='ges', belegt=gesq2)

    return error


def retry():

    error = []
    ignore_error = []
    profilbuchstabe = cache.read('profilbuchstabe', hash='session')

    if profilbuchstabe == 'A' or profilbuchstabe == 'B':

        polq1 = radio(request, 'polq1', ignore_error)
        polq2 = radio(request, 'polq2', ignore_error)

        if polq1 is not None:
            update_raster(['q11', 'q12', 'q21', 'q22'], fach='pol', reset=True)
            update_raster(['q11', 'q12'], fach='pol', belegt=polq1)
            if polq2 is not None:
                update_raster(['q21', 'q22'], fach='pol', belegt=polq2)

    if profilbuchstabe == 'C' or profilbuchstabe == 'D':

        gesq1 = radio(request, 'gesq1', ignore_error)
        gesq2 = radio(request, 'gesq2', ignore_error)

        if gesq1 is not None:
            update_raster(['q11', 'q12', 'q21', 'q22'], fach='ges', reset=True)
            update_raster(['q11', 'q12'], fach='ges', belegt=gesq1)
            if gesq2 is not None:
                update_raster(['q21', 'q22'], fach='ges', belegt=gesq2)

    if profilbuchstabe == 'E':

        polq1 = radio(request, 'polq1', ignore_error)
        polq2 = radio(request, 'polq2', ignore_error)
        gesq1 = radio(request, 'gesq1', ignore_error)
        gesq2 = radio(request, 'gesq2', ignore_error)

        if polq1 is not None or gesq1 is not None:

            if polq1 and not polq2:
                msg = "Sie müssen Politik in der Q-Phase durchgängig belegen."
                error.append(msg)
            elif not gesq1 and not polq1:
                msg = "Sie müssen entweder Geschichte in der Q1 oder Politik in der Q1 und Q2 belegen."
                error.append(msg)

        if polq1 is not None:
            update_raster(['q11', 'q12', 'q21', 'q22'], fach='pol', reset=True)
            update_raster(['q11', 'q12'], fach='pol', belegt=polq1)
            if polq2 is not None:
                update_raster(['q21', 'q22'], fach='pol', belegt=polq2)

        if gesq1 is not None:
            update_raster(['Q11', 'q12', 'q21', 'q22'], fach='ges', reset=True)
            update_raster(['Q11', 'q12'], fach='ges', belegt=gesq1)
            if gesq2 is not None:
                update_raster(['q21', 'q22'], fach='ges', belegt=gesq2)

    return error

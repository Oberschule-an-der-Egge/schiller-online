from flask import request

from src.services import cache
from src.views.macros import radio, select


def update_raster(halbjahre, fach=None, reset=False):

    stunden = 3

    # Kompletter Reset aller Fächer
    if reset:
        for fach in ['bio', 'che', 'phy']:
            for h in halbjahre:
                cache.delete(fach, hash=h)
    else:
        for h in halbjahre:
            cache.write(fach, stunden, hash=h)


def update_possiblepruefung():
    # Checken, welche NW nun tatsächlich in Q22 eingetragen wurde und diese als mögliche Prüfungsfächer definieren.
    # Praktischerweise wird beim erneuten Durchlauf der Methode auch automatisch resettet.

    if cache.read('phy', hash='q22'):
        cache.write('possiblepruefung', 'phy')
    else:
        cache.delete('possiblepruefung', 'phy')

    if cache.read('che', hash='q22'):
        cache.write('possiblepruefung', 'che')
    else:
        cache.delete('possiblepruefung', 'che')

    if cache.read('profilbuchstabe', hash='session') != 'D':
        if cache.read('bio', hash='q22'):
            cache.write('possiblepruefung', 'bio')
        else:
            cache.delete('possiblepruefung', 'bio')


def process():

    error = []
    ignore_error = []
    profilbuchstabe = cache.read('profilbuchstabe', hash='session')

    e11_nw1 = select(request, 'e11_nw1', error)
    e11_nw2 = select(request, 'e11_nw2', error)
    e12_nw1 = select(request, 'e12_nw1', ignore_error)
    e12_nw2 = select(request, 'e12_nw2', ignore_error)
    q11_nw2 = radio(request, 'q11_nw2', ignore_error)  # Profil D wählt Q11 nicht aus
    q21_nw2 = radio(request, 'q21_nw2', ignore_error)

    if e11_nw1 == e11_nw2:
        error.append('NaWi 1 und NaWi 2 müssen sich unterscheiden.')

    if not error:
        update_raster(['e11'], fach=e11_nw1)
        update_raster(['e11'], fach=e11_nw2)

    if profilbuchstabe == 'A' and not error:
        update_raster(['e12', 'q11', 'q12', 'q21', 'q22'], fach=e12_nw1)
        update_raster(['e12'], fach=e12_nw2)
    else:
        e12_nw1 = 'bio'
        if profilbuchstabe == 'D':
            e12_nw2 = 'che'
        if e12_nw1 is not None and e12_nw2 is not None:
            update_raster(['e12'], fach=e12_nw1)
            update_raster(['e12'], fach=e12_nw2)

    if profilbuchstabe != 'D' and q11_nw2 is None:
        msg = 'Q11 NaWi 2 muss ausgefüllt sein.'
        error.append(msg)

    if q11_nw2 and not error:
        update_raster(['q11', 'q12'], fach=e12_nw2)
        if q21_nw2:
            update_raster(['q21', 'q22'], fach=e12_nw2)

    return error


def retry():

    error = []
    ignore_error = []
    profilbuchstabe = cache.read('profilbuchstabe', hash='session')

    e11_nw1 = select(request, 'e11_nw1', ignore_error)
    e11_nw2 = select(request, 'e11_nw2', ignore_error)
    e12_nw1 = select(request, 'e12_nw1', ignore_error)
    e12_nw2 = select(request, 'e12_nw2', ignore_error)

    if e12_nw2 is not None:
        q11_nw2 = radio(request, 'q11_nw2', error)
        q21_nw2 = radio(request, 'q21_nw2', ignore_error)

        if profilbuchstabe == 'A':
            if not error:
                if e12_nw1 and e12_nw2:
                    update_raster(['e12', 'q11', 'q12', 'q21', 'q22'], fach=e12_nw1)
                    update_raster(['e12'], fach=e12_nw2)
                else:
                    msg = "NaWi-Fächer für E1 und E2 müssen ausgewählt werden."
                    error.append(msg)
        else:
            e12_nw1 = 'bio'
            if profilbuchstabe == 'D':
                e12_nw2 = 'che'
            if e12_nw1 is not None and e12_nw2 is not None:
                update_raster(['e12'], fach=e12_nw1)
                update_raster(['e12'], fach=e12_nw2)

        if q11_nw2 and not error:
            update_raster(['q11', 'q12', 'q21', 'q22'], reset=True)
            update_raster(['q11', 'q12'], fach=e12_nw2)
            if q21_nw2:
                update_raster(['q21', 'q22'], fach=e12_nw2)

    return error

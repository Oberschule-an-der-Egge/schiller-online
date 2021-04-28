from flask import request

from src.services import cache
from src.views.macros import radio, select


def update_raster(halbjahre, reset=False, fremdsprache=None, sprachanfaenger=None):

    if sprachanfaenger:
        stunden = 4
    else:
        stunden = 3

    if reset:
        for fremdsprache in ['fra', 'lat', 'spa', 'rus', 'tur']:
            for h in halbjahre:
                cache.delete(fremdsprache, hash=h)
    else:
        for h in halbjahre:
            cache.write(fremdsprache, stunden, hash=h)


def update_possiblepruefung(halbjahre, fremdsprache):

    # Prüfen, ob alle erforderlichen >Prüfungshalbjahre< in >Halbjahre< enthalten sind.
    pruefungshalbjahre = ["e12", "q11", "q12", "q21", "q22"]
    if set(pruefungshalbjahre).issubset(halbjahre):
        cache.write('possiblepruefung', fremdsprache)
    else:
        cache.delete('possiblepruefung', fremdsprache)


def process():

    error = []
    ignore_error = []

    belegverpflichtung = radio(request, 'belegverpflichtung', error)
    freiwillig = None
    fremdsprache = select(request, 'fremdsprache', ignore_error)
    sprachanfaenger = True

    if not belegverpflichtung:
        freiwillig = radio(request, 'freiwillig', error)
        sprachanfaenger = radio(request, 'anfaenger', ignore_error, 'anfaenger', 'fortsetzer')

    if not belegverpflichtung and not freiwillig:
        # Keine Fremdsprache eintragen
        pass
    else:
        if fremdsprache is None:
            # Fremdsprache wurde nicht ausgewaehlt (wurde oben ignoriert)
            msg = "Bitte wählen Sie eine Fremdsprache aus."
            error.append(msg)
        else:
            update_raster(['e11', 'e12', 'q11', 'q12', 'q21', 'q22'], fremdsprache=fremdsprache, sprachanfaenger=sprachanfaenger)
            update_possiblepruefung(['e11', 'e12', 'q11', 'q12', 'q21', 'q22'], fremdsprache)

    cache.write(hash='session', mapping={
        'fremdsprache': str(fremdsprache),
        'freiwilligefremdsprache': str(freiwillig),
    })

    return error


def retry():

    error = []
    ignore_error = []

    belegverpflichtung = radio(request, 'belegverpflichtung', ignore_error)
    fremdsprache = select(request, 'fremdsprache', ignore_error)
    sprachanfaenger = False

    if belegverpflichtung is not None:
        if not belegverpflichtung:
            freiwillig = radio(request, 'freiwillig', error)
            sprachanfaenger = radio(request, 'anfaenger', ignore_error, 'anfaenger', 'fortsetzer')

        if not belegverpflichtung and not freiwillig:
            # Keine Fremdsprache eintragen
            pass
        else:
            if fremdsprache is None:
                # Fremdsprache wurde nicht ausgewaehlt (wurde oben ignoriert)
                msg = "Bitte wählen Sie eine Fremdsprache aus."
                error.append(msg)
            else:
                update_raster(['e11', 'e12', 'q11', 'q12', 'q21', 'q22'], reset=True)
                update_raster(['e11', 'e12', 'q11', 'q12', 'q21', 'q22'], fremdsprache=fremdsprache, sprachanfaenger=sprachanfaenger)
                update_possiblepruefung(['e11', 'e12', 'q11', 'q12', 'q21', 'q22'], fremdsprache)

    return error

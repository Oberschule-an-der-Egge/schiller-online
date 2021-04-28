from flask import request

from src.services import cache
from src.views.macros import select


def process():

    error = []
    profilbuchstabe = cache.read('profilbuchstabe', hash='session')
    freierlk = cache.read('freierlk', hash='session')

    pruefung1 = request.form.get('pruefung1')
    pruefung2 = request.form.get('pruefung2')

    if profilbuchstabe == 'E' and freierlk != 'mat':
        pruefung3 = 'mat'
        pruefung4 = select(request, 'pruefung4', error)
    else:
        pruefung3 = select(request, 'pruefung3', error)
        pruefung4 = select(request, 'pruefung4', error)

    if not error:
        # Kombination der Pruefungsfaecher ueberpruefen
        error.extend(pruefen_pruefungsfaecher([pruefung1, pruefung2, pruefung3, pruefung4]))

    if not error:
        update_pruefungsfaecher(pruefung3)
        update_pruefungsfaecher(pruefung4)

    return error


def pruefen_pruefungsfaecher(fachliste):

    error = []
    feldliste = {cache.read_static_hash(fach, hash='fach_feld') for fach in fachliste}

    # Check: Alle drei Aufgabenfelder abgedeckt
    if not {'agf1', 'agf2', 'agf3'}.issubset(feldliste):
        error.append('Prüfungsfächer müssen über alle drei Aufgabenfelder verteilt sein.')

    # Check: Alle Kernfächer abgedeckt
    if 'deu' in fachliste:
        if 'eng' in fachliste or 'mat' in fachliste:
            pass
    elif 'eng' in fachliste:
        if 'deu' in fachliste or 'mat' in fachliste:
            pass
    elif 'mat' in fachliste:
        if 'eng' in fachliste or 'deu' in fachliste:
            pass
    else:
        error.append('Zwei der drei Kernfächer müssen Prüfungsfächer sein.')

    return error


def update_pruefungsfaecher(fach):
    cache.write('pruefungsfaecher', fach)

from flask import request, current_app
from src.services import cache
from src.views.macros import radio, text, select


def process():
    """Process the form data entered at step1()
    Todo: Errors with None.strip() and msa
    """
    error = []

    vorname = text(request, 'vorname', error).strip()
    nachname = text(request, 'nachname', error).strip()
    jahrgang = current_app.config['JAHRGANG']
    klasse = select(request, 'klasse', error)
    msa = radio(request, 'msa', error)
    profil = select(request, 'profilbuchstabe', error)
    freierlk = select(request, 'freierlk', error)
    pflichtstundenzahl = radio(request, 'pflichtstundenzahl', error, 'g8', 'g9')

    cache.write(hash='session', mapping={
        'vorname': vorname,
        'nachname': nachname,
        'jahrgang': jahrgang,
        'klasse': klasse,
        'profilbuchstabe': profil,
        'freierlk': freierlk,
        'msa': str(msa),
    })

    if (profil == 'A' and freierlk == 'deu') \
            or (profil == 'B' and freierlk == 'eng') \
            or (profil == 'C' and freierlk == 'pae'):
        error.append('Profil und Freier LK müssen sich unterscheiden.')

    if pflichtstundenzahl:
        stunden = 136
    else:
        stunden = 124

    if not error:
        cache.write('pflichtstundenzahl', stunden, hash='session')

    return error

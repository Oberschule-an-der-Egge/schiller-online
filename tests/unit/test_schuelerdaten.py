def test_schuelerdaten_profil_freierlk_not_equal(client):
    kwargs = {
        'vorname': 'Thorsten',
        'nachname': 'Torte',
        'klasse': '20A',
        'profilbuchstabe': 'A',
        'freierlk': 'deu',
        'msa': 'ja',
        'pflichtstundenzahl': 'g8',
    }
    rv = client.post('/', data=kwargs)
    assert b'Profil und Freier LK' in rv.data


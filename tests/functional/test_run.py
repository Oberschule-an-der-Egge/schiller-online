import pytest

from src.services import generate_pdf

profil_a = {
    'step1': {
        'vorname': 'Christian',
        'nachname': 'Macht',
        'klasse': '20a',
        'profilbuchstabe': 'A',  # Deutsch
        'freierlk': 'eng',
        'msa': 'ja',
        'pflichtstundenzahl': 'g8',
    },
    'step2': {
        'belegverpflichtung': 'ja',
        'fremdsprache': 'fra',
        'kuenstlerischesfach_e11': 'kun',
        'e11_nw1': 'bio',
        'e11_nw2': 'phy',
        'e12_nw1': 'bio',
        'e12_nw2': 'che',
        'q11_nw2': 'ja',
        'q21_nw2': 'ja',
    },
    'step3': {
        'info': 'ja',
        'polq1': 'nein',
        # 'polq2': 'nein',
        'psye1': 'nein',
        'psye2': 'nein',
        'paeq1': 'ja',
        'paeq2': 'ja',
        'geoe1': 'nein',
        'geoe2': 'ja',
        'geoq1': 'ja',
        'geoq2': 'nein',
    },
    'step4': {
        'action': 'keep',
    },
    'step5': {
        'pruefung1': 'deu',
        'pruefung2': 'eng',
        'pruefung3': 'bio',
        'pruefung4': 'pae',
    },
}

profil_b = {
    'step1': {
        'vorname': 'Christian',
        'nachname': 'Macht',
        'klasse': '20a',
        'profilbuchstabe': 'B',  # Englisch
        'freierlk': 'pae',
        'msa': 'ja',
        'pflichtstundenzahl': 'g8',
    },
    'step2': {
        'belegverpflichtung': 'nein',
        'freiwillig': 'ja',
        'fremdsprache': 'rus',
        'anfaenger': 'anfaenger',  # anfaenger | fortsetzer
        'kuenstlerischesfach_e11': 'mus',
        'kuenstlerischesfach_e12': 'dar',
        'e11_nw1': 'bio',
        'e11_nw2': 'phy',
        'e12_nw2': 'che',
        'q11_nw2': 'ja',
        'q21_nw2': 'ja',
    },
    'step3': {
        'info': 'ja',
        'polq1': 'nein',
        # 'polq2': 'nein',
        'psye1': 'nein',
        'psye2': 'nein',
        'paeq1': 'ja',
        'paeq2': 'ja',
        'geoe1': 'nein',
        'geoe2': 'ja',
        'geoq1': 'ja',
        'geoq2': 'nein',
    },
    'step4': {
        'action': 'keep',  # keep | retry
    },
    'step5': {
        'pruefung1': 'eng',
        'pruefung2': 'pae',
        'pruefung3': 'bio',
        'pruefung4': 'pae',
    },
}

profil_c = {
    'step1': {
        'vorname': 'Christian',
        'nachname': 'Macht',
        'klasse': '20a',
        'profilbuchstabe': 'C',  # Paedagogik
        'freierlk': 'eng',
        'msa': 'nein',
        'pflichtstundenzahl': 'g8',
    },
    'step2': {
        'belegverpflichtung': 'nein',
        'freiwillig': 'ja',
        'fremdsprache': 'spa',
        'anfaenger': 'fortsetzer',  # anfaenger | fortsetzer
        'kuenstlerischesfach_e11': 'dar',
        'kuenstlerischesfach_e12': 'dar',
        'e11_nw1': 'bio',
        'e11_nw2': 'phy',
        'e12_nw2': 'phy',
        'q11_nw2': 'ja',
        'q21_nw2': 'ja',
    },
    'step3': {
        'info': 'ja',
        'gesq1': 'ja',
        'gesq2': 'ja',
        'psye1': 'nein',
        'psye2': 'ja',
        'psyq1': 'ja',
        'psyq2': 'nein',
        'geoe1': 'nein',
        'geoe2': 'nein',
    },
    'step4': {
        # 'action': 'keep',  # keep | retry
        'gesq1': 'nein',
        'psye1': 'nein',
        'psye2': 'ja',
        'psyq1': 'nein',
        'action': 'retry',  # sollte 150 Wochenstunden sein
    },
    'step5': {
        'pruefung1': 'pae',
        'pruefung2': 'eng',
        'pruefung3': 'bio',
        'pruefung4': 'pol',
    },
}

profil_e = {
    'step1': {
        'vorname': 'Christian',
        'nachname': 'Macht',
        'klasse': '20a',
        'profilbuchstabe': 'E',  # Sport
        'freierlk': 'pae',
        'msa': 'nein',
        'pflichtstundenzahl': 'g8',
    },
    'step2': {
        'belegverpflichtung': 'nein',
        'freiwillig': 'ja',
        'fremdsprache': 'fra',
        'anfaenger': 'anfaenger',  # anfaenger | fortsetzer
        'kuenstlerischesfach_e11': 'dar',
        'kuenstlerischesfach_e12': 'dar',
        'e11_nw1': 'bio',
        'e11_nw2': 'phy',
        'e12_nw2': 'phy',
        'q11_nw2': 'nein',
    },
    'step3': {
        'info': 'ja',
        'gesq1': 'ja',
        'polq1': 'ja',
        'polq2': 'ja',
        'psye1': 'nein',
        'psye2': 'nein',
        'geoe1': 'nein',
        'geoe2': 'nein',
    },
    'step4': {
        'action': 'keep',  # keep | retry
    },
    'step5': {
        'pruefung1': 'spx',
        'pruefung2': 'pae',
        'pruefung3': 'mat',
        'pruefung4': 'eng',
    },
}


@pytest.mark.parametrize('test_input, wochenstunden', [(profil_a, 166), (profil_b, 160), (profil_e, 152)])
def test_full_run(client, monkeypatch, test_input, wochenstunden):
    rv = client.get('/')
    step1 = test_input['step1']
    rv = client.post('/', data=step1, follow_redirects=True)
    assert b'Schritt 2 (20%)' in rv.data
    assert b'Wahl der <span class="fach">Fremdsprache</span>' in rv.data
    step2 = test_input['step2']
    rv = client.post('/2', data=step2, follow_redirects=True)
    assert b'Schritt 3 (40%)' in rv.data
    assert b'Bitte geben Sie Informationen zu Informatik an:' in rv.data
    step3 = test_input['step3']
    rv = client.post('/3', data=step3, follow_redirects=True)
    assert b'Schritt 4 (60%)' in rv.data
    # print('actual wochenstunden:', rv.data.partition(b'betr\xc3\xa4gt nun ')[2][:3].decode('utf-8'))
    assert f'Ihre Wochenstundenzahl in den 4 Halbjahren der Q-Phase beträgt nun {wochenstunden}.'.encode('utf-8') in rv.data
    step4 = test_input['step4']
    rv = client.post('/4', data=step4, follow_redirects=True )
    assert b'Schritt 5 (80%)' in rv.data
    assert b'1. Pr\xc3\xbcfungsfach' in rv.data
    step5 = test_input['step5']
    rv = client.post('/5', data=step5, follow_redirects=True)
    assert b'Ihr \xc3\x9c-Plan wurde erfolgreich erzeugt!' in rv.data
    assert b'als PDF herunterladen' in rv.data
    rv = client.get('/output')
    assert rv.status_code == 200


@pytest.mark.parametrize('test_input, wochenstunden', [(profil_c, (168, 150))])
def test_full_run_retry(client, monkeypatch, test_input, wochenstunden):
    rv = client.get('/')
    step1 = test_input['step1']
    rv = client.post('/', data=step1, follow_redirects=True)
    assert b'Schritt 2 (20%)' in rv.data
    assert b'Wahl der <span class="fach">Fremdsprache</span>' in rv.data
    step2 = test_input['step2']
    rv = client.post('/2', data=step2, follow_redirects=True)
    assert b'Schritt 3 (40%)' in rv.data
    assert b'Bitte geben Sie Informationen zu Informatik an:' in rv.data
    step3 = test_input['step3']
    rv = client.post('/3', data=step3, follow_redirects=True)
    for wst in wochenstunden:
        if wst == wochenstunden[-1]:
            rv = client.post('/4', data={'action': 'keep'}, follow_redirects=True)
        else:
            assert b'Schritt 4 (60%)' in rv.data
            # print('actual wochenstunden:', rv.data.partition(b'betr\xc3\xa4gt nun ')[2][:3].decode('utf-8'))
            assert f'Ihre Wochenstundenzahl in den 4 Halbjahren der Q-Phase beträgt nun {wst}.'.encode('utf-8') in rv.data
            step4 = test_input['step4']
            rv = client.post('/4', data=step4, follow_redirects=True)
    assert b'Schritt 5 (80%)' in rv.data
    assert b'1. Pr\xc3\xbcfungsfach' in rv.data
    step5 = test_input['step5']
    rv = client.post('/5', data=step5, follow_redirects=True)
    assert b'Ihr \xc3\x9c-Plan wurde erfolgreich erzeugt!' in rv.data
    assert b'als PDF herunterladen' in rv.data
    rv = client.get('/output')
    assert rv.status_code == 200

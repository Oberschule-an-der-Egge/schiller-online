from time import sleep

from helium import *


def test_full():
    driver = start_chrome('localhost:5000/', headless=False)

    # Step1
    assert driver.current_url == 'http://localhost:5000/'
    write('Christian', into='Vorname')
    write('Macht', into='Nachname')
    select('Klasse', '20a')
    select('Profil', 'A - Deutsch')
    select('Freier LK', 'Pädagogik')
    # click(RadioButton('Ja'))
    click(RadioButton('Nein'))
    # click(RadioButton('Nach der 10. Klasse (G9)'))
    click(RadioButton('Nach der 9. Klasse (G8)'))
    click('Weiter zu Schritt 2')
    assert driver.current_url == 'http://localhost:5000/2'

    # Step2
    fremdsprache_nein = driver.find_element_by_id('belegverpflichtung_2')
    click(fremdsprache_nein)
    freiwillig_ja = driver.find_element_by_id('freiwillig_1')
    sleep(0.5)
    click(freiwillig_ja)
    select('Welche Sprache haben Sie neu angefangen?', 'Französisch')
    click(RadioButton('Sprach-Fortsetzer'))

    select('Welches künstlerisch-musische Fach haben Sie im 1. Halbjahr der E-Phase belegt?', 'Darstellendes Spiel')

    select('NaWi 1', 'Biologie')
    select('NaWi 2', 'Physik')
    select('Welche Naturwissenschaft haben Sie im 2. Halbjahr der E-Phase belegt, die sie bis zum Abitur fortsetzen möchten?', 'Biologie')
    select('Welche weitere Naturwissenschaft haben Sie im 2. Halbjahr der E-Phase belegt?', 'Physik')
    q11_nw2_nein = driver.find_element_by_id('q11_nw2_2')
    click(q11_nw2_nein)
    click('Weiter zu Schritt 3')
    assert driver.current_url == 'http://localhost:5000/3'

    # Step3
    info_ja = driver.find_element_by_id('info_1')
    click(info_ja)
    # gesq1_nein = driver.find_element_by_id('gesq1_2')
    # click(gesq1_nein)
    polq1_ja = driver.find_element_by_id('polq1_1')
    click(polq1_ja)
    sleep(0.5)
    polq2_ja = driver.find_element_by_id('polq2_1')
    click(polq2_ja)
    psye1_ja = driver.find_element_by_id('psye1_1')
    click(psye1_ja)
    psye2_ja = driver.find_element_by_id('psye2_1')
    click(psye2_ja)
    psyq1_ja = driver.find_element_by_id('psyq1_1')
    click(psyq1_ja)
    psyq2_ja = driver.find_element_by_id('psyq2_1')
    click(psyq2_ja)
    paeq1_nein = driver.find_element_by_id('paeq1_2')
    click(paeq1_nein)
    geoe1_nein = driver.find_element_by_id('geoe1_2')
    click(geoe1_nein)
    geoe2_nein = driver.find_element_by_id('geoe2_2')
    click(geoe2_nein)
    click('Weiter zu Schritt 4')
    assert driver.current_url == 'http://localhost:5000/4'

    # Step4
    click('Keine weiteren Änderungen vornehmen und fortfahren')
    assert driver.current_url == 'http://localhost:5000/5'

    # Step5
    pruefung3 = driver.find_element_by_id('pruefung3')
    select(pruefung3, 'Geschichte')
    pruefung4 = driver.find_element_by_id('pruefung4')
    select(pruefung4, 'Mathe')
    click('Ü-Plan erstellen')
    assert driver.current_url == 'http://localhost:5000/6'

    # Step6
    click('Ü-Plan ansehen')
    assert driver.current_url == 'http://localhost:5000/output'

    # kill_browser()



def test_sportprofil():
    driver = start_chrome('localhost:5000/', headless=False)

    # Step1
    assert driver.current_url == 'http://localhost:5000/'
    write('Christian', into='Vorname')
    write('Macht', into='Nachname')
    select('Klasse', '20a')
    select('Profil', 'E - Sport')
    select('Freier LK', 'Pädagogik')
    # click(RadioButton('Ja'))
    click(RadioButton('Nein'))
    # click(RadioButton('Nach der 10. Klasse (G9)'))
    click(RadioButton('Nach der 9. Klasse (G8)'))
    click('Weiter zu Schritt 2')
    assert driver.current_url == 'http://localhost:5000/2'

    # Step2
    fremdsprache_nein = driver.find_element_by_id('belegverpflichtung_2')
    click(fremdsprache_nein)
    freiwillig_ja = driver.find_element_by_id('freiwillig_1')
    sleep(0.5)
    click(freiwillig_ja)
    select('Welche Sprache haben Sie neu angefangen?', 'Französisch')
    click(RadioButton('Sprach-Anfänger'))

    select('Welches künstlerisch-musische Fach haben Sie im 1. Halbjahr der E-Phase belegt?', 'Darstellendes Spiel')
    select('Welches künstlerisch-musische Fach haben Sie im 2. Halbjahr der E-Phase belegt?', 'Darstellendes Spiel')

    select('NaWi 1', 'Biologie')
    select('NaWi 2', 'Physik')
    select('Welche Naturwissenschaft haben Sie neben Biologie im zweiten Halbjahr der E-Phase belegt?', 'Physik')
    sleep(0.5)
    q11_nw2_nein = driver.find_element_by_id('q11_nw2_2')
    click(q11_nw2_nein)
    click('Weiter zu Schritt 3')
    assert driver.current_url == 'http://localhost:5000/3'

    # Step3
    info_ja = driver.find_element_by_id('info_1')
    click(info_ja)
    # gesq1_nein = driver.find_element_by_id('gesq1_2')
    # click(gesq1_nein)
    gesq1_nein = driver.find_element_by_id('gesq1_2')
    click(gesq1_nein)
    polq1_ja = driver.find_element_by_id('polq1_1')
    click(polq1_ja)
    sleep(0.5)
    polq2_ja = driver.find_element_by_id('polq2_1')
    click(polq2_ja)
    psye1_ja = driver.find_element_by_id('psye1_1')
    click(psye1_ja)
    psye2_ja = driver.find_element_by_id('psye2_1')
    click(psye2_ja)
    psyq1_ja = driver.find_element_by_id('psyq1_1')
    click(psyq1_ja)
    psyq2_ja = driver.find_element_by_id('psyq2_1')
    click(psyq2_ja)
    geoe1_nein = driver.find_element_by_id('geoe1_2')
    click(geoe1_nein)
    geoe2_nein = driver.find_element_by_id('geoe2_2')
    click(geoe2_nein)
    click('Weiter zu Schritt 4')
    assert driver.current_url == 'http://localhost:5000/4'

    # Step4
    click('Keine weiteren Änderungen vornehmen und fortfahren')
    assert driver.current_url == 'http://localhost:5000/5'

    # Step5
    pruefung4 = driver.find_element_by_id('pruefung4')
    select(pruefung4, 'Englisch')
    click('Ü-Plan erstellen')
    assert driver.current_url == 'http://localhost:5000/6'

    # Step6
    click('Ü-Plan ansehen')
    assert driver.current_url == 'http://localhost:5000/output'

    # kill_browser()

if __name__ == "__main__":
    print("Everything passed")
import json
import os

import xlsxwriter
from flask import session, current_app

from src.services import cache


def create_xlsx(filename):
    """Excel Datei mit korrekten Daten und Formatierung erstellen.
    :return: URI der xlsx
    """

    output_path = current_app.config['OUTPUT_PATH']
    filename_xlsx = '{}.xlsx'.format(filename)
    filepath_xlsx = os.path.join(output_path, filename_xlsx)

    r = cache.RedisConnection()

    # Prepare data for xlsx
    session_hash = 'session:{}'.format(session['token'])

    if r.hget(session_hash, 'msa') == 'True':
        msa = True
    else:
        msa = False

    if r.hget(session_hash, 'toggleinfo') == 'True':
        toggleinfo = True
    else:
        toggleinfo = False

    fs_short = r.hget(session_hash, 'fremdsprache')
    fremdsprache = r.hget('fach_short_long', fs_short)
    kf_short = r.hget(session_hash, 'kuenstlerischesfach')
    kuenstlerischesfach = r.hget('fach_short_long', kf_short)

    stundensumme = {h: r.hget('stundensumme:' + session['token'], h) for h in
                    ['e11', 'e12', 'q11', 'q12', 'q21', 'q22']}
    stundensumme.update({'e_phase': r.hget('stundensumme:' + session['token'], 'e_phase')})
    stundensumme.update({'q_phase': r.hget('stundensumme:' + session['token'], 'q_phase')})

    workbook = workbook_generieren(
        filepath=filepath_xlsx,
        schuelername='{}, {}'.format(r.hget(session_hash, 'nachname'), r.hget(session_hash, 'vorname')),
        profil=r.hget(session_hash, 'profilbuchstabe'),
        jahrgang=r.hget(session_hash, 'jahrgang'),
        msa=msa,
        klasse=r.hget(session_hash, 'klasse'),
        pruefungsfaecher=list(r.smembers('pruefungsfaecher:' + session['token'])),
        pflichtstundenzahl=r.hget(session_hash, 'pflichtstundenzahl'),
    )
    workbook_fuellen(
        workbook=workbook,
        raster=json.loads(r.get('raster:' + session['token'])),
        profil=r.hget(session_hash, 'profilbuchstabe'),
        pruefungsfaecher=list(r.smembers('pruefungsfaecher:' + session['token'])),
        stundensumme=stundensumme,
        toggleinfo=toggleinfo,
        fremdsprache=fremdsprache,
        kuenstlerischesfach=kuenstlerischesfach,
    )

    if os.environ.get('FLASK_ENV') == 'production':
        filepath_xlsx = current_app.config['URL_UPLAN'] + filename_xlsx

    return filepath_xlsx


def get_workbook(filepath):
    """Separiert, um Override beim Testen zu ermöglichen
    """
    return xlsxwriter.Workbook(filepath)


def workbook_generieren(
        filepath=None,
        schuelername=None,
        profil=None,
        jahrgang=None,
        msa=None,
        klasse=None,
        pruefungsfaecher=None,
        pflichtstundenzahl=None,
):

    # Worksheet öffnen
    workbook = get_workbook(filepath)
    worksheet = workbook.add_worksheet('Uebersichtsplan')  # Sheet1

    # Worksheet auf Querformat stellen
    worksheet.set_landscape()

    # Formatierungen definieren:
    worksheet.set_column('A:A', 11.25)
    worksheet.set_column('AB:AB', 11.25)
    worksheet.set_column('B:AA', 3)
    worksheet.set_row(3, 58)
    worksheet.set_row(1, 24)
    kopfzeilenformatfett = workbook.add_format({'bold': True, 'font_size': 18})
    schuelernamensformat = workbook.add_format({'font_size': 18, "align": "right"})
    fetteueberschrift = workbook.add_format({'bold': True, 'font_size': 12, "bottom": 5, "valign": "top"})
    klassenformat = workbook.add_format({'bold': True, 'font_size': 12, "align": "right", "bottom": 5, "valign": "top"})
    zentrierteecken = workbook.add_format(
        {"left": 5, "right": 5, "align": "center", "valign": "vcenter", 'font_size': 10, "bold": True,
         'text_wrap': True})
    stundenzahlformatierung = workbook.add_format(
        {"align": "center", "valign": "vcenter", 'font_size': 14, "top": 1, "right": 1, "bottom": 1})
    stundenzahlformatierungmitlinielinks = workbook.add_format(
        {"align": "center", "valign": "vcenter", 'font_size': 14, "left": 5, "top": 1, "right": 1, "bottom": 1})
    stundenzahlformatierungmitlinielinksundoben = workbook.add_format(
        {"align": "center", "valign": "vcenter", 'font_size': 14, "left": 5, "right": 1, "bottom": 1, "top": 5})
    stundenzahlformatierungmitlinielinksundobenundrechts = workbook.add_format(
        {"align": "center", "valign": "vcenter", 'font_size': 14, "left": 5, "right": 5, "bottom": 1, "top": 5})
    pflichstundenformatierung = workbook.add_format(
        {"align": "center", "valign": "vcenter", 'font_size': 14, "top": 5, "right": 1, "bottom": 5})
    faecherzeilenformat = workbook.add_format({'bold': True, "rotation": 90, "bottom": 5, "right": 1})
    faecherzeilenformatmitrandlinks = workbook.add_format({'bold': True, "rotation": 90, "bottom": 5, "left": 5})
    aufgabenfeldformat = workbook.add_format(
        {'bold': True, 'font_size': 12, "bottom": 2, "left": 5, "right": 5, "align": "center"})
    kapitel = workbook.add_format({"top": 5, "left": 5, "right": 5})
    fettelinieuntenundoben = workbook.add_format({"bottom": 5, "top": 5})
    zentriertklein = workbook.add_format({'font_size': 8, "align": "center"})

    # Borderpatrol: Rahmen zeichnen
    fetterrahmenunten = workbook.add_format({"bottom": 5})
    fetterrahmenlinks = workbook.add_format({"left": 5})
    fetterrahmenoben = workbook.add_format({"top": 5})
    for i in range(0, 28):
        worksheet.write(1, i, "", fetterrahmenunten)
    for i in range(2, 15):
        worksheet.write(i, 28, "", fetterrahmenlinks)
    for i in range(0, 28):
        worksheet.write(15, i, "", fetterrahmenoben)

    # Rahmen prophylaktisch zeichnen, da unklar ist, ob die Zellen beschrieben werden:
    for i in range(2, 15):
        worksheet.write(i, 11, "", fetterrahmenlinks)
    for i in range(2, 15):
        worksheet.write(i, 17, "", fetterrahmenlinks)
    for i in range(2, 15):
        worksheet.write(i, 21, "", fetterrahmenlinks)
    for i in range(2, 15):
        worksheet.write(i, 22, "", fetterrahmenlinks)
    for i in range(2, 15):
        worksheet.write(i, 24, "", fetterrahmenlinks)
    for i in range(5, 7):
        for h in range(1, 27):
            worksheet.write(i, h, "", stundenzahlformatierung)
    for i in range(8, 10):
        for h in range(1, 27):
            worksheet.write(i, h, "", stundenzahlformatierung)
    for i in range(11, 13):
        for h in range(1, 27):
            worksheet.write(i, h, "", stundenzahlformatierung)
    for h in range(1, 27):
        worksheet.write(14, h, "", stundenzahlformatierung)
    worksheet.write("L15", "", stundenzahlformatierungmitlinielinks)
    worksheet.write("R15", "", stundenzahlformatierungmitlinielinks)
    worksheet.write("V15", "", stundenzahlformatierungmitlinielinks)
    worksheet.write("W15", "", stundenzahlformatierungmitlinielinks)
    for i in range(5, 15):
        worksheet.write(i, 11, "", stundenzahlformatierungmitlinielinks)
    for i in range(5, 15):
        worksheet.write(i, 21, "", stundenzahlformatierungmitlinielinks)

    # Fette Trennlinien zwischen den Jahrgängen zeichnen
    for i in range(1, 28):
        worksheet.write(4, i, "", fettelinieuntenundoben)
    for i in range(1, 28):
        worksheet.write(7, i, "", fettelinieuntenundoben)
    for i in range(1, 28):
        worksheet.write(10, i, "", fettelinieuntenundoben)
    for i in range(1, 28):
        worksheet.write(13, i, "", fettelinieuntenundoben)

    # Rahmen von einzelnen Zellen, die immer leer sind zeichnen:
    worksheet.write("A3", "", kapitel)
    worksheet.write("A5", "", kapitel)
    worksheet.write("AB5", "", kapitel)
    worksheet.write("AB3", "", kapitel)
    worksheet.merge_range('Y15:AB15', '', kapitel)
    worksheet.write("AB11", "", stundenzahlformatierungmitlinielinksundobenundrechts)
    worksheet.write("Y12", "", stundenzahlformatierungmitlinielinks)
    worksheet.write("Y13", "", stundenzahlformatierungmitlinielinks)
    worksheet.write("AB11", "", stundenzahlformatierungmitlinielinksundoben)

    # Überschriftszeilen
    worksheet.write(0, 0, f"Übersichtsplan für die Schullaufbahn  - Profil {profil} - Jg. {jahrgang}", kopfzeilenformatfett)
    worksheet.write("AB1", schuelername, schuelernamensformat)
    if msa:
        worksheet.write(1, 0, "mit MSA", fetteueberschrift)
    elif not msa:
        worksheet.write(1, 0, "ohne MSA", fetteueberschrift)
    worksheet.write("AB2", f"aus Klasse: {klasse}", klassenformat)

    # LinkeSpaltegenerieren
    # Definition der Sonderformatierungen
    centermitdach = workbook.add_format({"top": 5, "left": 5, "right": 5, 'align': 'center', "valign": "vcenter"})
    center = workbook.add_format({"left": 5, "right": 5, "top": 1, 'align': 'center'})
    tiefgestellt = workbook.add_format({'font_script': 2, "font_size": 18, "bold": True})
    fett18 = workbook.add_format({'font_size': 18, "bold": True})
    worksheet.write_rich_string('A6', ' ', fett18, "E", tiefgestellt, "1" ' ', centermitdach)
    worksheet.write_rich_string('A7', ' ', fett18, "E", tiefgestellt, "2" ' ', center)
    worksheet.write("A8", "", centermitdach)
    worksheet.write_rich_string('A9', ' ', fett18, "Q", tiefgestellt, "1.1" ' ', centermitdach)
    worksheet.write_rich_string('A10', ' ', fett18, "Q", tiefgestellt, "1.2" ' ', center)
    worksheet.write("A11", "", centermitdach)
    worksheet.write_rich_string('A12', ' ', fett18, "Q", tiefgestellt, "2.1" ' ', centermitdach)
    worksheet.write_rich_string('A13', ' ', fett18, "Q", tiefgestellt, "2.2" ' ', center)
    worksheet.write("A14", "", centermitdach)
    worksheet.write_rich_string("A15", " ", fett18, "A", " ", centermitdach)

    # Zellen für Aufgabenfelder mergen und beschriften:
    worksheet.merge_range('B3:K3', 'Aufgabenfeld I', aufgabenfeldformat)
    worksheet.merge_range('L3:Q3', 'Aufgabenfeld II', aufgabenfeldformat)
    worksheet.merge_range('R3:U3', 'Aufgabenfeld III', aufgabenfeldformat)
    worksheet.write("V3", "o. A.", aufgabenfeldformat)
    worksheet.merge_range('W3:X3', 'Sport', aufgabenfeldformat)
    worksheet.merge_range('Y3:AA3', 'Lernzeit', aufgabenfeldformat)

    # Ecken der Tabelle Generieren
    worksheet.merge_range("A3:A4", "Leistungsfach/ \nGrundfach", zentrierteecken)
    worksheet.merge_range("AB3:AB4", "Stunden - \nsumme", zentrierteecken)

    # Überschriften für die Spalten eintragen:
    # Aufgabenfeld I
    worksheet.write("B4", "Deutsch", faecherzeilenformat)
    worksheet.write("C4", "Englisch", faecherzeilenformat)
    worksheet.write("D4", "Französisch", faecherzeilenformat)
    worksheet.write("E4", "Latein", faecherzeilenformat)
    worksheet.write("F4", "Spanisch", faecherzeilenformat)
    worksheet.write("G4", "Russisch", faecherzeilenformat)
    worksheet.write("H4", "Türkisch", faecherzeilenformat)
    worksheet.write("I4", "Darstellendes Spiel", faecherzeilenformat)
    worksheet.write("J4", "Kunst", faecherzeilenformat)
    worksheet.write("K4", "Musik", faecherzeilenformat)

    # Aufgabenfeld II
    worksheet.write("M4", "Politik", faecherzeilenformat)
    worksheet.write("N4", "Geographie", faecherzeilenformat)
    worksheet.write("O4", "Pädagogik", faecherzeilenformat)
    worksheet.write("P4", "Psychologie", faecherzeilenformat)
    worksheet.write("Q4", "Religion", faecherzeilenformat)

    # Aufgabenfeld III
    worksheet.write("S4", "Physik", faecherzeilenformat)
    worksheet.write("T4", "Chemie", faecherzeilenformat)
    worksheet.write("U4", "Biologie", faecherzeilenformat)

    # Sport
    worksheet.write("X4", "Theorie", faecherzeilenformat)

    # Pseudounterricht
    worksheet.write("Z4", "Selbstlernz.", faecherzeilenformat)
    worksheet.write("AA4", "Projekt", faecherzeilenformat)

    # Überschrieben derjenigen Fächer, die eine linie Links benötigen
    # Stumpf ist Trumpf:
    worksheet.write("L4", "Geschichte", faecherzeilenformatmitrandlinks)
    worksheet.write("R4", "Mathematik", faecherzeilenformatmitrandlinks)
    worksheet.write("V4", "Informatik", faecherzeilenformatmitrandlinks)
    worksheet.write("W4", "Praxis", faecherzeilenformatmitrandlinks)
    worksheet.write("Y4", "Methoden", faecherzeilenformatmitrandlinks)
    # for col_num, data in enumerate(pruefungsfaecher):
    #    worksheet.write(col_num, 1, data)

    # Unterschriftenzeile Generieren
    worksheet.write("A18", "____________________________________________")
    worksheet.write("R18", "________________________________________________")
    worksheet.write("A19", "Unterschrift Schüler/in: Ü-Plan erhalten")
    worksheet.write("R19", "Datum, Unterschrift: Erziehungsberechtigte/r")
    """
    #Hinweis für Übermittlung des Plans mergen und eintragen:
    worksheet.merge_range("A21:AB21", "Senden Sie einen unterschriebenen Scan dieser Tabelle bitte umgehend an:"
                                      " Christopher.Driebe@schulverwaltung.bremen.de", zentriertklein)
    worksheet.merge_range("A22:AB22", "Postalisch können Sie den Plan an folgende Adresse übermitteln:"
                                      " Oberschule an der Egge; c/o Christopher Driebe; Eggestedter Strasse 20;"
                                      " 28779 Bremen", zentriertklein)
    """

    # Einfügen der Mindeststundenzahlen in die Tabelle
    worksheet.write("U8", "Stundensumme E-Phase (mind. 70h)", pflichstundenformatierung)
    worksheet.write("U14", f"Stundensumme Q-Phase (mind. {pflichtstundenzahl})", pflichstundenformatierung)

    return workbook


def workbook_fuellen(
        workbook=None,
        raster=None,
        profil=None,
        pruefungsfaecher=None,
        stundensumme=None,
        toggleinfo=None,
        fremdsprache=None,
        kuenstlerischesfach=None,
):

    worksheet = workbook.get_worksheet_by_name('Uebersichtsplan')
    worksheet.activate()

    # Formatierung definieren
    stundenzahlformatierung = workbook.add_format(
        {"align": "center", "valign": "vcenter", 'font_size': 14, "top": 1, "right": 1, "bottom": 1})
    stundenzahlformatierungmitlinielinks = workbook.add_format(
        {"align": "center", "valign": "vcenter", 'font_size': 14, "left": 5, "top": 1, "right": 1, "bottom": 1})
    stundenzahlformatierungmitlinielinksundrechts = workbook.add_format(
        {"align": "center", "valign": "vcenter", 'font_size': 14, "left": 5, "top": 1, "right": 5, "bottom": 1})
    stundenzahlformatierungmitlinielinksundobenundrechts = workbook.add_format(
        {"align": "center", "valign": "vcenter", 'font_size': 14, "left": 5, "right": 5, "bottom": 1, "top": 5})

    # Deutschstunden eintragen
    worksheet.write(5, 1, raster["Aufgabenfeld I"]["Deutsch"]["E11"], stundenzahlformatierung)
    worksheet.write(6, 1, raster["Aufgabenfeld I"]["Deutsch"]["E12"], stundenzahlformatierung)
    worksheet.write(8, 1, raster["Aufgabenfeld I"]["Deutsch"]["Q11"], stundenzahlformatierung)
    worksheet.write(9, 1, raster["Aufgabenfeld I"]["Deutsch"]["Q12"], stundenzahlformatierung)
    worksheet.write(11, 1, raster["Aufgabenfeld I"]["Deutsch"]["Q21"], stundenzahlformatierung)
    worksheet.write(12, 1, raster["Aufgabenfeld I"]["Deutsch"]["Q22"], stundenzahlformatierung)

    # Englischstunden eintragen
    worksheet.write(5, 2, raster["Aufgabenfeld I"]["Englisch"]["E11"], stundenzahlformatierung)
    worksheet.write(6, 2, raster["Aufgabenfeld I"]["Englisch"]["E12"], stundenzahlformatierung)
    worksheet.write(8, 2, raster["Aufgabenfeld I"]["Englisch"]["Q11"], stundenzahlformatierung)
    worksheet.write(9, 2, raster["Aufgabenfeld I"]["Englisch"]["Q12"], stundenzahlformatierung)
    worksheet.write(11, 2, raster["Aufgabenfeld I"]["Englisch"]["Q21"], stundenzahlformatierung)
    worksheet.write(12, 2, raster["Aufgabenfeld I"]["Englisch"]["Q22"], stundenzahlformatierung)

    # Mathestunden eintragen
    worksheet.write(5, 17, raster["Aufgabenfeld III"]["Mathe"]["E11"], stundenzahlformatierungmitlinielinks)
    worksheet.write(6, 17, raster["Aufgabenfeld III"]["Mathe"]["E12"], stundenzahlformatierungmitlinielinks)
    worksheet.write(8, 17, raster["Aufgabenfeld III"]["Mathe"]["Q11"], stundenzahlformatierungmitlinielinks)
    worksheet.write(9, 17, raster["Aufgabenfeld III"]["Mathe"]["Q12"], stundenzahlformatierungmitlinielinks)
    worksheet.write(11, 17, raster["Aufgabenfeld III"]["Mathe"]["Q21"], stundenzahlformatierungmitlinielinks)
    worksheet.write(12, 17, raster["Aufgabenfeld III"]["Mathe"]["Q22"], stundenzahlformatierungmitlinielinks)

    # NW-Stunden eintragen
    # Physik
    if raster["Aufgabenfeld III"]["Physik"]["E11"]:
        worksheet.write(5, 18, raster["Aufgabenfeld III"]["Physik"]["E11"], stundenzahlformatierung)
    if raster["Aufgabenfeld III"]["Physik"]["E12"]:
        worksheet.write(6, 18, raster["Aufgabenfeld III"]["Physik"]["E12"], stundenzahlformatierung)
    if raster["Aufgabenfeld III"]["Physik"]["Q11"]:
        worksheet.write(8, 18, raster["Aufgabenfeld III"]["Physik"]["Q11"], stundenzahlformatierung)
    if raster["Aufgabenfeld III"]["Physik"]["Q12"]:
        worksheet.write(9, 18, raster["Aufgabenfeld III"]["Physik"]["Q12"], stundenzahlformatierung)
    if raster["Aufgabenfeld III"]["Physik"]["Q21"]:
        worksheet.write(11, 18, raster["Aufgabenfeld III"]["Physik"]["Q21"], stundenzahlformatierung)
    if raster["Aufgabenfeld III"]["Physik"]["Q22"]:
        worksheet.write(12, 18, raster["Aufgabenfeld III"]["Physik"]["Q22"], stundenzahlformatierung)

    # Chemie
    if raster["Aufgabenfeld III"]["Chemie"]["E11"]:
        worksheet.write(5, 19, raster["Aufgabenfeld III"]["Chemie"]["E11"], stundenzahlformatierung)
    if raster["Aufgabenfeld III"]["Chemie"]["E12"]:
        worksheet.write(6, 19, raster["Aufgabenfeld III"]["Chemie"]["E12"], stundenzahlformatierung)
    if raster["Aufgabenfeld III"]["Chemie"]["Q11"]:
        worksheet.write(8, 19, raster["Aufgabenfeld III"]["Chemie"]["Q11"], stundenzahlformatierung)
    if raster["Aufgabenfeld III"]["Chemie"]["Q12"]:
        worksheet.write(9, 19, raster["Aufgabenfeld III"]["Chemie"]["Q12"], stundenzahlformatierung)
    if raster["Aufgabenfeld III"]["Chemie"]["Q21"]:
        worksheet.write(11, 19, raster["Aufgabenfeld III"]["Chemie"]["Q21"], stundenzahlformatierung)
    if raster["Aufgabenfeld III"]["Chemie"]["Q22"]:
        worksheet.write(12, 19, raster["Aufgabenfeld III"]["Chemie"]["Q22"], stundenzahlformatierung)

    # Biologie
    if raster["Aufgabenfeld III"]["Biologie"]["E11"]:
        worksheet.write(5, 20, raster["Aufgabenfeld III"]["Biologie"]["E11"], stundenzahlformatierung)
    if raster["Aufgabenfeld III"]["Biologie"]["E12"]:
        worksheet.write(6, 20, raster["Aufgabenfeld III"]["Biologie"]["E12"], stundenzahlformatierung)
    if raster["Aufgabenfeld III"]["Biologie"]["Q11"]:
        worksheet.write(8, 20, raster["Aufgabenfeld III"]["Biologie"]["Q11"], stundenzahlformatierung)
    if raster["Aufgabenfeld III"]["Biologie"]["Q12"]:
        worksheet.write(9, 20, raster["Aufgabenfeld III"]["Biologie"]["Q12"], stundenzahlformatierung)
    if raster["Aufgabenfeld III"]["Biologie"]["Q21"]:
        worksheet.write(11, 20, raster["Aufgabenfeld III"]["Biologie"]["Q21"], stundenzahlformatierung)
    if raster["Aufgabenfeld III"]["Biologie"]["Q22"]:
        worksheet.write(12, 20, raster["Aufgabenfeld III"]["Biologie"]["Q22"], stundenzahlformatierung)

    # Religion Eintragen:
    worksheet.write(8, 16, raster["Aufgabenfeld II"]["Religion"]["Q11"], stundenzahlformatierung)
    worksheet.write(9, 16, raster["Aufgabenfeld II"]["Religion"]["Q12"], stundenzahlformatierung)

    # Informatik Eintragen:
    if toggleinfo:
        if raster["o. A."]["Informatik"]["E11"]:
            worksheet.write(5, 21, raster["o. A."]["Informatik"]["E11"], stundenzahlformatierungmitlinielinks)
        if raster["o. A."]["Informatik"]["E12"]:
            worksheet.write(6, 21, raster["o. A."]["Informatik"]["E12"], stundenzahlformatierungmitlinielinks)
        if raster["o. A."]["Informatik"]["Q11"]:
            worksheet.write(8, 21, raster["o. A."]["Informatik"]["Q11"], stundenzahlformatierungmitlinielinks)
        if raster["o. A."]["Informatik"]["Q12"]:
            worksheet.write(9, 21, raster["o. A."]["Informatik"]["Q12"], stundenzahlformatierungmitlinielinks)
        if raster["o. A."]["Informatik"]["Q21"]:
            worksheet.write(11, 21, raster["o. A."]["Informatik"]["Q21"], stundenzahlformatierungmitlinielinks)
        if raster["o. A."]["Informatik"]["Q22"]:
            worksheet.write(12, 21, raster["o. A."]["Informatik"]["Q22"], stundenzahlformatierungmitlinielinks)

    # Sporttheorie und Sportpraxis eintragen:
    # TODO: Was ist, wenn jemand in der E-Phase das Sportprofil gewechselt hat?
    # Praxis:
    worksheet.write(5, 22, raster["Sport"]["Praxis"]["E11"], stundenzahlformatierungmitlinielinks)
    worksheet.write(6, 22, raster["Sport"]["Praxis"]["E12"], stundenzahlformatierungmitlinielinks)
    worksheet.write(8, 22, raster["Sport"]["Praxis"]["Q11"], stundenzahlformatierungmitlinielinks)
    worksheet.write(9, 22, raster["Sport"]["Praxis"]["Q12"], stundenzahlformatierungmitlinielinks)
    worksheet.write(11, 22, raster["Sport"]["Praxis"]["Q21"], stundenzahlformatierungmitlinielinks)
    worksheet.write(12, 22, raster["Sport"]["Praxis"]["Q22"], stundenzahlformatierungmitlinielinks)

    # Theorie:
    if profil == "E":
        worksheet.write(5, 23, raster["Sport"]["Theorie"]["E11"], stundenzahlformatierung)
        worksheet.write(6, 23, raster["Sport"]["Theorie"]["E12"], stundenzahlformatierung)
        worksheet.write(8, 23, raster["Sport"]["Theorie"]["Q11"], stundenzahlformatierung)
        worksheet.write(9, 23, raster["Sport"]["Theorie"]["Q12"], stundenzahlformatierung)
        worksheet.write(11, 23, raster["Sport"]["Theorie"]["Q21"], stundenzahlformatierung)
        worksheet.write(12, 23, raster["Sport"]["Theorie"]["Q22"], stundenzahlformatierung)

    # Lernzeitstunden eintragen:
    # Methode
    worksheet.write(5, 24, raster["Lernzeit"]["Methoden"]["E11"], stundenzahlformatierungmitlinielinks)
    worksheet.write(6, 24, raster["Lernzeit"]["Methoden"]["E12"], stundenzahlformatierungmitlinielinks)
    worksheet.write(8, 24, raster["Lernzeit"]["Methoden"]["Q11"], stundenzahlformatierungmitlinielinks)
    worksheet.write(9, 24, raster["Lernzeit"]["Methoden"]["Q12"], stundenzahlformatierungmitlinielinks)

    # Selbstlernzeit
    worksheet.write(5, 25, raster["Lernzeit"]["Selbstlernzeit"]["E11"], stundenzahlformatierung)
    worksheet.write(6, 25, raster["Lernzeit"]["Selbstlernzeit"]["E12"], stundenzahlformatierung)
    worksheet.write(8, 25, raster["Lernzeit"]["Selbstlernzeit"]["Q11"], stundenzahlformatierung)
    worksheet.write(9, 25, raster["Lernzeit"]["Selbstlernzeit"]["Q12"], stundenzahlformatierung)

    # Projektstunden
    worksheet.write(5, 26, raster["Lernzeit"]["Projektstunden"]["E11"], stundenzahlformatierung)
    worksheet.write(6, 26, raster["Lernzeit"]["Projektstunden"]["E12"], stundenzahlformatierung)
    worksheet.write(8, 26, raster["Lernzeit"]["Projektstunden"]["Q11"], stundenzahlformatierung)
    worksheet.write(9, 26, raster["Lernzeit"]["Projektstunden"]["Q12"], stundenzahlformatierung)

    # Fremdsprachenstunden eintragen
    if not fremdsprache:
        print("Überspringe Fremdspracheneintragung nach Excel, da keine Fremdsprache gewählt")
    elif fremdsprache:
        if fremdsprache == "Französisch":
            fuerfremdsprachebenoetigtespalte = 3
        if fremdsprache == "Latein":
            fuerfremdsprachebenoetigtespalte = 4
        if fremdsprache == "Spanisch":
            fuerfremdsprachebenoetigtespalte = 5
        if fremdsprache == "Russisch":
            fuerfremdsprachebenoetigtespalte = 6
        if fremdsprache == "Türkisch":
            fuerfremdsprachebenoetigtespalte = 7
        worksheet.write(5, fuerfremdsprachebenoetigtespalte, raster["Aufgabenfeld I"][fremdsprache]["E11"], stundenzahlformatierung)
        worksheet.write(6, fuerfremdsprachebenoetigtespalte, raster["Aufgabenfeld I"][fremdsprache]["E12"], stundenzahlformatierung)
        if raster["Aufgabenfeld I"][fremdsprache]["Q11"] != 0:
            worksheet.write(8, fuerfremdsprachebenoetigtespalte, raster["Aufgabenfeld I"][fremdsprache]["Q11"], stundenzahlformatierung)
        if raster["Aufgabenfeld I"][fremdsprache]["Q12"] != 0:
            worksheet.write(9, fuerfremdsprachebenoetigtespalte, raster["Aufgabenfeld I"][fremdsprache]["Q12"], stundenzahlformatierung)
        if raster["Aufgabenfeld I"][fremdsprache]["Q21"] != 0:
            worksheet.write(11, fuerfremdsprachebenoetigtespalte, raster["Aufgabenfeld I"][fremdsprache]["Q21"], stundenzahlformatierung)
        if raster["Aufgabenfeld I"][fremdsprache]["Q22"] != 0:
            worksheet.write(12, fuerfremdsprachebenoetigtespalte, raster["Aufgabenfeld I"][fremdsprache]["Q22"], stundenzahlformatierung)
    else:
        print("Es gab ein Problem beim Eintragen der Fremdsprache in die Exceltabelle: Keine wohldefninierte Fremdsprache")

    # Künstlerisch-Musische Stunden Eintragen
    if raster["Aufgabenfeld I"]["Kunst"]["E11"] != 0:
        worksheet.write(5, 9, raster["Aufgabenfeld I"]["Kunst"]["E11"], stundenzahlformatierung)
    if raster["Aufgabenfeld I"]["Darstellendes Spiel"]["E11"] != 0:
        worksheet.write(5, 8, raster["Aufgabenfeld I"]["Darstellendes Spiel"]["E11"], stundenzahlformatierung)
    if raster["Aufgabenfeld I"]["Musik"]["E11"] != 0:
        worksheet.write(5, 10, raster["Aufgabenfeld I"]["Musik"]["E11"], stundenzahlformatierung)
    fuermusischesfachbenoetigtespalte = 0
    if profil == "A":
        fuerfremdsprachebenoetigtespalte = 9
        worksheet.write(6, 9, raster["Aufgabenfeld I"][kuenstlerischesfach]["E12"], stundenzahlformatierung)
        worksheet.write(8, 9, raster["Aufgabenfeld I"][kuenstlerischesfach]["Q11"], stundenzahlformatierung)
        worksheet.write(9, 9, raster["Aufgabenfeld I"][kuenstlerischesfach]["Q12"], stundenzahlformatierung)
        worksheet.write(11, 9, raster["Aufgabenfeld I"][kuenstlerischesfach]["Q21"], stundenzahlformatierung)
        worksheet.write(12, 9, raster["Aufgabenfeld I"][kuenstlerischesfach]["Q22"], stundenzahlformatierung)
    elif kuenstlerischesfach == "Kunst":
        worksheet.write(6, 9, raster["Aufgabenfeld I"][kuenstlerischesfach]["E12"], stundenzahlformatierung)
        worksheet.write(8, 9, raster["Aufgabenfeld I"][kuenstlerischesfach]["Q11"], stundenzahlformatierung)
        worksheet.write(9, 9, raster["Aufgabenfeld I"][kuenstlerischesfach]["Q12"], stundenzahlformatierung)
    elif kuenstlerischesfach == "Musik":
        worksheet.write(6, 10, raster["Aufgabenfeld I"][kuenstlerischesfach]["E12"], stundenzahlformatierung)
        worksheet.write(8, 10, raster["Aufgabenfeld I"][kuenstlerischesfach]["Q11"], stundenzahlformatierung)
        worksheet.write(9, 10, raster["Aufgabenfeld I"][kuenstlerischesfach]["Q12"], stundenzahlformatierung)
    elif kuenstlerischesfach == "Darstellendes Spiel":
        worksheet.write(6, 8, raster["Aufgabenfeld I"][kuenstlerischesfach]["E12"], stundenzahlformatierung)
        worksheet.write(8, 8, raster["Aufgabenfeld I"][kuenstlerischesfach]["Q11"], stundenzahlformatierung)
        worksheet.write(9, 8, raster["Aufgabenfeld I"][kuenstlerischesfach]["Q12"], stundenzahlformatierung)
    else:
        print("Es gab einen Fehler beim Eintragen Ihres künsterlisch-musischen Faches! Ihre Eingabe %s war ungültig" % kuenstlerischesfach)

    # Geschichte und Politk eintragen:
    # Geschichte
    worksheet.write("L6", raster["Aufgabenfeld II"]["Geschichte"]["E11"], stundenzahlformatierungmitlinielinks)
    worksheet.write("L7", raster["Aufgabenfeld II"]["Geschichte"]["E12"], stundenzahlformatierungmitlinielinks)
    if raster["Aufgabenfeld II"]["Geschichte"]["Q11"]:
        worksheet.write("L9", raster["Aufgabenfeld II"]["Geschichte"]["Q11"], stundenzahlformatierungmitlinielinks)
    if raster["Aufgabenfeld II"]["Geschichte"]["Q12"]:
        worksheet.write("L10", raster["Aufgabenfeld II"]["Geschichte"]["Q12"], stundenzahlformatierungmitlinielinks)
    if raster["Aufgabenfeld II"]["Geschichte"]["Q21"]:
        worksheet.write("L12", raster["Aufgabenfeld II"]["Geschichte"]["Q21"], stundenzahlformatierungmitlinielinks)
    if raster["Aufgabenfeld II"]["Geschichte"]["Q22"]:
        worksheet.write("L13", raster["Aufgabenfeld II"]["Geschichte"]["Q22"], stundenzahlformatierungmitlinielinks)

    # Politik
    worksheet.write("M6", raster["Aufgabenfeld II"]["Politik"]["E11"], stundenzahlformatierung)
    worksheet.write("M7", raster["Aufgabenfeld II"]["Politik"]["E12"], stundenzahlformatierung)
    if raster["Aufgabenfeld II"]["Politik"]["Q11"]:
        worksheet.write("M9", raster["Aufgabenfeld II"]["Politik"]["Q11"], stundenzahlformatierung)
    if raster["Aufgabenfeld II"]["Politik"]["Q12"]:
        worksheet.write("M10", raster["Aufgabenfeld II"]["Politik"]["Q12"], stundenzahlformatierung)
    if raster["Aufgabenfeld II"]["Politik"]["Q21"]:
        worksheet.write("M12", raster["Aufgabenfeld II"]["Politik"]["Q21"], stundenzahlformatierung)
    if raster["Aufgabenfeld II"]["Politik"]["Q22"]:
        worksheet.write("M13", raster["Aufgabenfeld II"]["Politik"]["Q22"], stundenzahlformatierung)

    # Geographie eintragen:
    if raster["Aufgabenfeld II"]["Geographie"]["E11"]:
        worksheet.write("N6", raster["Aufgabenfeld II"]["Geographie"]["E11"], stundenzahlformatierung)
    if raster["Aufgabenfeld II"]["Geographie"]["E12"]:
        worksheet.write("N7", raster["Aufgabenfeld II"]["Geographie"]["E12"], stundenzahlformatierung)
    if raster["Aufgabenfeld II"]["Geographie"]["Q11"]:
        worksheet.write("N9", raster["Aufgabenfeld II"]["Geographie"]["Q11"], stundenzahlformatierung)
    if raster["Aufgabenfeld II"]["Geographie"]["Q12"]:
        worksheet.write("N10", raster["Aufgabenfeld II"]["Geographie"]["Q12"], stundenzahlformatierung)
    if raster["Aufgabenfeld II"]["Geographie"]["Q21"]:
        worksheet.write("N12", raster["Aufgabenfeld II"]["Geographie"]["Q21"], stundenzahlformatierung)
    if raster["Aufgabenfeld II"]["Geographie"]["Q22"]:
        worksheet.write("N13", raster["Aufgabenfeld II"]["Geographie"]["Q22"], stundenzahlformatierung)

    # Pädagogik eintragen:
    if raster["Aufgabenfeld II"]["Pädagogik"]["E11"]:
        worksheet.write("O6", raster["Aufgabenfeld II"]["Pädagogik"]["E11"], stundenzahlformatierung)
    if raster["Aufgabenfeld II"]["Pädagogik"]["E12"]:
        worksheet.write("O7", raster["Aufgabenfeld II"]["Pädagogik"]["E12"], stundenzahlformatierung)
    if raster["Aufgabenfeld II"]["Pädagogik"]["Q11"]:
        worksheet.write("O9", raster["Aufgabenfeld II"]["Pädagogik"]["Q11"], stundenzahlformatierung)
    if raster["Aufgabenfeld II"]["Pädagogik"]["Q12"]:
        worksheet.write("O10", raster["Aufgabenfeld II"]["Pädagogik"]["Q12"], stundenzahlformatierung)
    if raster["Aufgabenfeld II"]["Pädagogik"]["Q21"]:
        worksheet.write("O12", raster["Aufgabenfeld II"]["Pädagogik"]["Q21"], stundenzahlformatierung)
    if raster["Aufgabenfeld II"]["Pädagogik"]["Q22"]:
        worksheet.write("O13", raster["Aufgabenfeld II"]["Pädagogik"]["Q22"], stundenzahlformatierung)

    # Psychologie eintragen:
    if raster["Aufgabenfeld II"]["Psychologie"]["E11"]:
        worksheet.write("P6", raster["Aufgabenfeld II"]["Psychologie"]["E11"], stundenzahlformatierung)
    if raster["Aufgabenfeld II"]["Psychologie"]["E12"]:
        worksheet.write("P7", raster["Aufgabenfeld II"]["Psychologie"]["E12"], stundenzahlformatierung)
    if raster["Aufgabenfeld II"]["Psychologie"]["Q11"]:
        worksheet.write("P9", raster["Aufgabenfeld II"]["Psychologie"]["Q11"], stundenzahlformatierung)
    if raster["Aufgabenfeld II"]["Psychologie"]["Q12"]:
        worksheet.write("P10", raster["Aufgabenfeld II"]["Psychologie"]["Q12"], stundenzahlformatierung)
    if raster["Aufgabenfeld II"]["Psychologie"]["Q21"]:
        worksheet.write("P12", raster["Aufgabenfeld II"]["Psychologie"]["Q21"], stundenzahlformatierung)
    if raster["Aufgabenfeld II"]["Psychologie"]["Q22"]:
        worksheet.write("P13", raster["Aufgabenfeld II"]["Psychologie"]["Q22"], stundenzahlformatierung)

    # Prüfungsfächer eintragen:
    if 'deu' in pruefungsfaecher:
        worksheet.write("B15", "X", stundenzahlformatierung)
    if 'eng' in pruefungsfaecher:
        worksheet.write("C15", "X", stundenzahlformatierung)
    if 'fra' in pruefungsfaecher:
        worksheet.write("D15", "X", stundenzahlformatierung)
    if 'lat' in pruefungsfaecher:
        worksheet.write("E15", "X", stundenzahlformatierung)
    if 'spa' in pruefungsfaecher:
        worksheet.write("F15", "X", stundenzahlformatierung)
    if 'rus' in pruefungsfaecher:
        worksheet.write("G15", "X", stundenzahlformatierung)
    if 'tur' in pruefungsfaecher:
        worksheet.write("H15", "X", stundenzahlformatierung)
    if 'dar' in pruefungsfaecher:
        worksheet.write("I15", "X", stundenzahlformatierung)
    if 'kun' in pruefungsfaecher:
        worksheet.write("J15", "X", stundenzahlformatierung)
    if 'mus' in pruefungsfaecher:
        worksheet.write("K15", "X", stundenzahlformatierung)
    if 'ges' in pruefungsfaecher:
        worksheet.write("L15", "X", stundenzahlformatierungmitlinielinks)
    if 'pol' in pruefungsfaecher:
        worksheet.write("M15", "X", stundenzahlformatierung)
    if 'geo' in pruefungsfaecher:
        worksheet.write("N15", "X", stundenzahlformatierung)
    if 'pae' in pruefungsfaecher:
        worksheet.write("O15", "X", stundenzahlformatierung)
    if 'psy' in pruefungsfaecher:
        worksheet.write("P15", "X", stundenzahlformatierung)
    if 'mat' in pruefungsfaecher:
        worksheet.write("R15", "X", stundenzahlformatierungmitlinielinks)
    if 'phy' in pruefungsfaecher:
        worksheet.write("S15", "X", stundenzahlformatierung)
    if 'che' in pruefungsfaecher:
        worksheet.write("T15", "X", stundenzahlformatierung)
    if 'bio' in pruefungsfaecher:
        worksheet.write("U15", "X", stundenzahlformatierung)
    if 'inf' in pruefungsfaecher:
        worksheet.write("V15", "X", stundenzahlformatierungmitlinielinks)
    if 'spx' in pruefungsfaecher:
        worksheet.write("W15", "X", stundenzahlformatierungmitlinielinks)
    if 'sth' in pruefungsfaecher:
        worksheet.write("X15", "X", stundenzahlformatierung)

    # Stundensummen final rechts eintragen
    worksheet.write("AB6", stundensumme["e11"], stundenzahlformatierungmitlinielinksundobenundrechts)
    worksheet.write("AB7", stundensumme["e12"], stundenzahlformatierungmitlinielinksundrechts)
    worksheet.write("AB8", stundensumme["e_phase"], stundenzahlformatierungmitlinielinksundobenundrechts)
    worksheet.write("AB9", stundensumme["q11"], stundenzahlformatierungmitlinielinksundobenundrechts)
    worksheet.write("AB10", stundensumme["q12"], stundenzahlformatierungmitlinielinksundrechts)
    worksheet.write("AB11", "", stundenzahlformatierungmitlinielinksundobenundrechts)
    worksheet.write("AB12", stundensumme["q21"], stundenzahlformatierungmitlinielinksundobenundrechts)
    worksheet.write("AB13", stundensumme["q22"], stundenzahlformatierungmitlinielinksundrechts)
    worksheet.write("AB14", stundensumme["q_phase"], stundenzahlformatierungmitlinielinksundobenundrechts)

    if toggleinfo:
        print("InformatikerInnen sind die coolsten!")

    workbook.close()

    return workbook


def pdf_konvertieren():
    """
    Excel Datei in eine PDF umwandeln.
    http://code.activestate.com/recipes/579128-convert-microsot-excel-xlsx-to-pdf-with-python-and/
    :return:
    """

    return None


def versenden():
    """
    Notification mailen, dass Plan erstellt wurde.
    :return:
    """
    pass

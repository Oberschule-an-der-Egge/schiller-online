import uuid

from flask import Blueprint, request, session, flash, redirect, url_for, render_template, current_app, jsonify, g

from src.models.generate_raster import generate_possiblepruefung, generate_pruefungsfaecher, generate_raster, \
    generate_freierlk
from src.services.logging import log_user_session
from src.services.mailing import Email
from src.views import review
from src.views.abfragen import fremdsprache, kuenstlerischesfach, naturwissenschaft, schuelerdaten, informatik, \
    geschichtepolitik, psychologie, paedagogik, geographie, pruefungsfach, easter_egg
from src.services import generate_pdf, cache, generate_excel

bp = Blueprint('form', __name__)


@bp.context_processor
def inject_for_all_templates():
    return dict(version=current_app.config['VERSION'])


@bp.route('/', methods=('GET', 'POST'))
def step1():
    """Step 1 - Get user data, set up session
    """

    # Helper for testing
    if session.get('reset'):
        session.clear()
        flash("Session zurückgesetzt.")

    # Initialise user session
    session['token'] = str(uuid.uuid4())
    cache.add_timestamp()

    if request.method == 'POST':

        error = schuelerdaten.process()

        if not error:
            session['reset'] = True
            generate_raster()
            generate_possiblepruefung()
            generate_pruefungsfaecher()
            generate_freierlk()
            return redirect(url_for('form.step2'))

        for e in error:
            flash(e)

    return render_template('step1.html')


@bp.route('/2', methods=('GET', 'POST'))
def step2():
    """Step 2 - Fremdsprachen, Kunst, NaWi
    """

    if not session.get('token'):
        flash('Fehler: Cookies müssen aktiviert sein.')
        return redirect(url_for('form.step1'))

    if not cache.set_exists('possiblepruefung'):
        flash('Bitte bei Schritt 1 beginnen.')
        return redirect(url_for('form.step1'))

    if request.method == 'POST':
        error = []
        error.extend(fremdsprache.process())
        error.extend(kuenstlerischesfach.process())
        error.extend(naturwissenschaft.process())
        naturwissenschaft.update_possiblepruefung()

        # Gimmick Step for special cases: Rebekka, Jule
        error.extend(easter_egg.process())

        if not error:
            return redirect(url_for('form.step3'))

        for e in error:
            flash(e)

    log_user_session()

    g.profilbuchstabe = cache.read('profilbuchstabe', hash='session')

    return render_template('step2.html')


@bp.route('/3', methods=('GET', 'POST'))
def step3():

    if not cache.set_exists('possiblepruefung'):
        flash('Bitte bei Schritt 1 beginnen.')
        return redirect(url_for('form.step1'))

    if request.method == 'POST':
        error = []
        error.extend(informatik.process())
        error.extend(geschichtepolitik.process())
        geschichtepolitik.update_possiblepruefung()
        error.extend(psychologie.process())
        error.extend(paedagogik.process())
        error.extend(geographie.process())

        if not error:
            return redirect(url_for('form.step4'))

        for e in error:
            flash(e)

    g.profilbuchstabe = cache.read('profilbuchstabe', hash='session')
    g.freierlk = cache.read('freierlk', hash='session')

    return render_template('step3.html')


@bp.route('/4', methods=('GET', 'POST'))
def step4():

    if not cache.set_exists('possiblepruefung'):
        flash('Bitte bei Schritt 1 beginnen.')
        return redirect(url_for('form.step1'))

    if request.form.get('action') == 'retry':
        error = []
        error.extend(geographie.retry())
        error.extend(geschichtepolitik.retry())
        geschichtepolitik.update_possiblepruefung()
        error.extend(paedagogik.retry())
        error.extend(psychologie.retry())
        error.extend(naturwissenschaft.retry())
        error.extend(fremdsprache.retry())

        for e in error:
            flash(e)

    elif request.form.get('action') == 'keep':
        return redirect(url_for('form.step5'))

    review.calculate_stundensumme()
    error, msg = review.check_stundensumme()

    g.profilbuchstabe = cache.read('profilbuchstabe', hash='session')
    if cache.read('freiwilligefremdsprache', hash='session') == 'True':
        g.freiwilligefremsprache = True
    else:
        g.freiwilligefremsprache = False

    g.freierlk = cache.read('freierlk', hash='session')
    g.has_geo = cache.read('geo', hash='e12')
    g.has_psy = cache.read('psy', hash='e12')

    return render_template('step4.html', error=error, msg=msg)


@bp.route('/5', methods=('GET', 'POST'))
def step5():

    if not cache.hash_exists('stundensumme'):
        flash('Bitte bei Schritt 1 beginnen.')
        return redirect(url_for('form.step1'))

    if request.method == 'POST':
        error = []
        error.extend(pruefungsfach.process())

        if not error:
            return redirect(url_for('form.step6'))

        for e in error:
            flash(e)

    # Create a dict() with all possible Pruefungsfaecher,
    # so we can use it in template creation
    pruefung_possible = {
        'Aufgabenfeld I': {},
        'Aufgabenfeld II': {},
        'Aufgabenfeld III': {},
    }

    r = cache.RedisConnection()
    profilbuchstabe = cache.read('profilbuchstabe', hash='session')
    freier_lk = cache.read('freierlk', hash='session')
    possiblepruefung = 'possiblepruefung:{}'.format(session['token'])
    pruefungsfaecher = 'pruefungsfaecher:{}'.format(session['token'])
    # https://redis.io/commands/SDIFF
    possible_diff = r.sdiff([possiblepruefung, pruefungsfaecher, 'e_profil'])

    for fach in possible_diff:
        if r.sismember('feld:agf1', fach):
            fach_long = cache.read_static_hash(fach, hash='fach_short_long')
            pruefung_possible['Aufgabenfeld I'].update({fach_long: fach})
        if r.sismember('feld:agf2', fach):
            fach_long = cache.read_static_hash(fach, hash='fach_short_long')
            pruefung_possible['Aufgabenfeld II'].update({fach_long: fach})
        if r.sismember('feld:agf3', fach):
            fach_long = cache.read_static_hash(fach, hash='fach_short_long')
            pruefung_possible['Aufgabenfeld III'].update({fach_long: fach})

    if profilbuchstabe == 'A':
        profil_lk = 'deu'
    elif profilbuchstabe == 'B':
        profil_lk = 'eng'
    elif profilbuchstabe == 'C':
        profil_lk = 'pae'
    elif profilbuchstabe == 'D':
        profil_lk = 'bio'
    elif profilbuchstabe == 'E':
        profil_lk = 'spx'

    g.plk_short = profil_lk
    g.plk_long = cache.read_static_hash(profil_lk, hash='fach_short_long')
    g.flk_short = freier_lk
    g.flk_long = cache.read_static_hash(freier_lk, hash='fach_short_long')
    g.profilbuchstabe = profilbuchstabe
    g.pruefung_possible = pruefung_possible

    return render_template('step5.html')


@bp.route('/6')
def step6():

    if not cache.hash_exists('stundensumme'):
        flash('Bitte bei Schritt 1 beginnen.')
        return redirect(url_for('form.step1'))

    # REDIS doesn't generate a raster, but it's needed for Generating Excel
    # and makes /output generation easier. Also legacy.

    raster = {}

    for feld, feld_long in zip(['agf1', 'agf2', 'agf3', 'oagf', 'spor', 'lern'], ['Aufgabenfeld I', 'Aufgabenfeld II', 'Aufgabenfeld III', 'o. A.', 'Sport', 'Lernzeit']):
        raster.update({feld_long: {}})
        for fach in cache.read_static_set('feld:' + feld):
            fach_long = cache.read_static_hash(fach, hash='fach_short_long')
            raster[feld_long].update({fach_long: {}})
            for h, h_long in zip(['e11', 'e12', 'q11', 'q12', 'q21', 'q22'], ['E11', 'E12', 'Q11', 'Q12', 'Q21', 'Q22']):
                value = cache.read(fach, hash=h)
                raster[feld_long][fach_long].update({h_long: value})

    cache.serialize('raster', raster)

    g.recipient = current_app.config['MAIL_RECIPIENT']

    vorname = cache.read('vorname', hash='session')
    nachname = cache.read('nachname', hash='session')
    jahrgang = cache.read('jahrgang', hash='session')
    klasse = cache.read('klasse', hash='session')
    filename = '{}-{}-{}'.format(nachname, vorname, session['token'][:8])

    g.download_pdf = generate_pdf.create_pdf(filename)
    download_xlsx = generate_excel.create_xlsx(filename)

    mail = Email(
        subject='[Schiller] Neuer Ü-Plan von {} {}'.format(vorname, nachname),
        text='Hurra!\n\n'
             f'{vorname} {nachname} ({jahrgang}{klasse}) hat einen neuen Ü-Plan erstellt:\n\n'
             f'Download PDF: {g.download_pdf} \n'
             f'Download XLSX: {download_xlsx} \n\n'
             f'Token: {session["token"]}\n\n'
             'In Liebe\n'
             'Schiller'
    )
    mail.send()

    return render_template('step6.html')


@bp.route('/output')
def output():

    if not cache.hash_exists('stundensumme'):
        flash('Redirect: Bitte bei Schritt 1 beginnen.')
        return redirect(url_for('form.step1'))

    g.profilbuchstabe = cache.read('profilbuchstabe', hash='session')
    g.jahrgang = cache.read('jahrgang', hash='session')
    g.klasse = cache.read('klasse', hash='session')
    g.schuelername = '{}, {}'.format(cache.read('nachname', hash='session'), cache.read('vorname', hash='session'))
    if cache.read('msa', hash='session') == 'True':
        g.msa = True
    else:
        g.msa = False

    g.stundensumme = {h: cache.read(h, hash='stundensumme')
                      for h in ['e11', 'e12', 'q11', 'q12', 'q21', 'q22']}
    g.stundensumme.update({'e_phase': cache.read('e_phase', hash='stundensumme')})
    g.stundensumme.update({'q_phase': cache.read('q_phase', hash='stundensumme')})
    g.raster = cache.deserialize('raster')
    g.pruefungsfaecher = list(cache.read('pruefungsfaecher'))
    g.token = session['token'][:8]

    return render_template('output.html')


@bp.route('/session')
def view_session():
    return jsonify(dict(session))


@bp.route('/redis')
def view_redis():
    r = cache.RedisConnection()
    redis_dict = dict()
    redis_dict['session'] = r.hgetall('session:' + session['token'])
    redis_dict['you_may_call_me_raster'] = dict()
    for h in ['e11', 'e12', 'q11', 'q12', 'q21', 'q22']:
        redis_dict['you_may_call_me_raster'][h] = r.hgetall(h + ':' + session['token'])
    redis_dict['possiblepruefung'] = list(r.smembers('possiblepruefung:' + session['token']))
    redis_dict['pruefungsfaecher'] = list(r.smembers('pruefungsfaecher:' + session['token']))
    redis_dict['stundensumme'] = r.hgetall('stundensumme:' + session['token'])
    # redis_dict['raster'] = r.get(cache.read('raster'))
    return jsonify(redis_dict)

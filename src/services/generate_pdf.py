import os
import weasyprint
from flask import session, render_template, g, current_app
import json

from src.services import cache


def create_pdf(filename):
    output_path = current_app.config['OUTPUT_PATH']
    filename_html = '{}.html'.format(filename)
    filename_pdf = '{}.pdf'.format(filename)
    filepath_html = os.path.join('output', filename_html)
    filepath_pdf = os.path.join(output_path, filename_pdf)

    create_html()
    save_html(filepath_html)
    convert_to_pdf(filepath_html, filepath_pdf)

    if os.environ.get('FLASK_ENV') == 'production':
        filepath_pdf = current_app.config['URL_UPLAN'] + filename_pdf

    return filepath_pdf


def create_html():
    r = cache.RedisConnection()

    session_hash = 'session:{}'.format(session['token'])
    g.profilbuchstabe = r.hget(session_hash, 'profilbuchstabe')
    g.jahrgang = r.hget(session_hash, 'jahrgang')
    g.klasse = r.hget(session_hash, 'klasse')
    g.schuelername = '{}, {}'.format(r.hget(session_hash, 'nachname'), r.hget(session_hash, 'vorname'))
    if r.hget(session_hash, 'msa') == 'True':
        g.msa = True
    else:
        g.msa = False
    g.stundensumme = {h: r.hget('stundensumme:' + session['token'], h)
                      for h in ['e11', 'e12', 'q11', 'q12', 'q21', 'q22']}
    g.stundensumme.update({'e_phase': r.hget('stundensumme:' + session['token'], 'e_phase')})
    g.stundensumme.update({'q_phase': r.hget('stundensumme:' + session['token'], 'q_phase')})
    g.raster = json.loads(r.get('raster:' + session['token']))
    g.pruefungsfaecher = list(r.smembers('pruefungsfaecher:' + session['token']))

    g.token = session['token'][:8]


def save_html(filepath):
    with open(filepath, 'w') as fout:
        fout.write(render_template('output.html'))


def convert_to_pdf(source, destination):
    weasyprint.HTML(source).write_pdf(destination)

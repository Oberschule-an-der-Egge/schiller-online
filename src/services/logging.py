from datetime import datetime

from flask import current_app, session

from src.services import cache


def log_user_session():
    logfile = current_app.config['LOG_FILE']
    with open(logfile, 'a+') as fout:
        token = session['token']
        now = datetime.utcnow()
        timestamp = now.strftime('%H:%M:%S %d.%m.%Y')
        vorname = cache.read('vorname', hash='session')
        nachname = cache.read('nachname', hash='session')
        line = '{} {} {} {}\n'.format(token, timestamp, vorname, nachname)
        fout.write(line)
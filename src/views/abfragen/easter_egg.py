from flask import request, session

from src.services import cache


def process():

    error = []

    vorname = cache.read('vorname', hash='session')
    iamspecial = request.form.get('iamspecial')

    if iamspecial:

        if iamspecial == 'jule':
            if vorname == 'Jule':
                cache.write('sth', 3, hash='e12')
                session['iamspecial'] = True
            else:
                error.append('Du bist nicht Jule.')

        if iamspecial == 'rebekka':
            if vorname == 'Rebekka':
                kfach = cache.read('kuenstlerischesfach', hash='session')
                if kfach == 'kun':
                    cache.write('dar', 2, hash='e11')
                    cache.write('dar', 2, hash='e12')
                elif kfach == 'dar':
                    cache.write('kun', 2, hash='e11')
                    cache.write('kun', 2, hash='e12')
                session['iamspecial'] = True
            else:
                error.append('Du bist nicht Rebekka.')

    return error

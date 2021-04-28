from flask import session
from src.services import cache


def calculate_stundensumme():

    r = cache.RedisConnection()

    def hash_name(h):
        return "{}:{}".format(h, session['token'])

    e_phase = list()
    for h in ['e11', 'e12']:
        values = r.hvals(hash_name(h))
        values_as_ints = list(map(int, values))
        summe = sum(values_as_ints)
        cache.write(h, summe, hash='stundensumme')
        e_phase.append(summe)
    cache.write('e_phase', sum(e_phase), hash='stundensumme')

    q_phase = list()
    for h in ['q11', 'q12', 'q21', 'q22']:
        values = r.hvals(hash_name(h))
        values_as_ints = list(map(int, values))
        summe = sum(values_as_ints)
        cache.write(h, summe, hash='stundensumme')
        q_phase.append(summe)
    cache.write('q_phase', sum(q_phase), hash='stundensumme')


def check_stundensumme():
    pflichtstunden = int(cache.read('pflichtstundenzahl', hash='session'))
    q_summe = int(cache.read('q_phase', hash='stundensumme'))
    differenz = q_summe - pflichtstunden
    durchschnitt = q_summe / 4

    msg = {}

    # Fall 1 - Zu wenige Stunden
    if q_summe < pflichtstunden:
        error = True
        msg.update(
            {'alert': "FEHLER: Sie haben nicht genug Wahlpflichfächer gewählt, um die Pflichtstundenzahl zu erfüllten.",
             'body': f"Die Pflichtstundenzahl beträgt für Sie in der Q-Phase {pflichtstunden} Stunden, "
                     f"Sie kommen jedoch nur auf {q_summe} Stunden. Bitte wählen Sie zusätzliche Fächer "
                     f"in der Q-Phase an, um Ihre Pflichtstundenzahl zu erfüllen."}
        )

    # Fall 2 - Mehr Stunden als gefordert oder genau so viele wie gefordert:
    elif q_summe >= pflichtstunden:
        error = False
        msg.update(
            {'alert': f"Ihre Wochenstundenzahl in den 4 Halbjahren der Q-Phase beträgt nun {q_summe}.",
             'body': f"Ihre Pflichtstundenzahl beträgt: {pflichtstunden} Stunden. "
                     f"Somit kämen Sie auf einen Durchschnitt von {durchschnitt} Unterrichtstunden pro Woche."}
        )

        # Fall 2.1: Mehr als empfohlen:
        if (pflichtstunden == 124 and differenz > 9) or q_summe >= 140:
            if q_summe > 148:
                msg.update(
                    {'hint1': "HINWEIS: Sie haben eine sehr hohe Anzahl an Stunden in der Q-Phase belegt. "
                              "Sind Sie sicher, dass Sie diese Stundenanzahl so beibehalten wollen?",
                     'hint2': "ACHTUNG: Sie können nach der Q1-Phase Fächer, die Sie nicht zwingend belegen müssen, "
                              "noch immer abwählen."}
                )
            else:
                msg.update(
                    {'hint1': "HINWEIS: Sie haben eine relativ hohe Anzahl an Stunden in der Q-Phase belegt. "
                              "Wenn Sie eine zweite Fremdsprache nachholen müssen, ist es jedoch möglich, "
                              "dass Sie Ihre Stundenanzahl nicht weiter verringern können. "
                              "Sind Sie sicher, dass Sie diese Stundenanzahl so beibehalten wollen?",
                     'hint2': "ACHTUNG: Sie können nach der Q1-Phase Fächer, die Sie nicht zwingend belegen müssen, "
                              "noch immer abwählen."}
                )

        # Fall 2.2: Weniger als empfohlen
        # Somit ist auch der Fall getroffen, dass ein Schüler exakt die Pflichtstundenzahl getroffen hat
        elif pflichtstunden == 124 and differenz <= 6:
            msg.update(
                {'hint1': "Sie haben kaum mehr Stunden gewählt, als Sie unbedingt belegen müssen. "
                          "HINWEIS: Manchmal ist es vorteilhaft, mehr Fächer als nötig zu belegen, "
                          "da man mit ihnen unter bestimmten Umständen leichter Unterkurse ausgleichen kann.",
                 'hint2': "ACHTUNG: Sie können einmal abgewählte Fächer nicht mehr aufnehmen."}
            )

        # Fall 2.3: Stundenzahl in der empfohlenen Toleranz
        elif (pflichtstunden == 124 and 6 < differenz <= 9) or (pflichtstunden == 136 and differenz <= 4):
            msg.update(
                {'hint1': "Ihre Stundenzahl liegt im empfohlenen Bereich. Bitte nehmen Sie jedoch folgendes zur Kenntnis:"
                          "\nManchmal ist es vorteilhaft, mehr Fächer als nötig zu belegen, "
                          "da man mit ihnen unter bestimmten Umständen leichter Unterkurse ausgleichen kann.",
                 'hint2': "Sie können einmal abgewählte Fächer nicht mehr aufnehmen."}
            )

        else:
            raise ValueError("Das sollte eigentlich nicht möglich sein.")

    return error, msg

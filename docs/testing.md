# Testing 

Die Tests für Schiller-Online sind mit `pytest` geschrieben. Um alle Tests auszuführen und die Codeabdeckung ("Coverage",
wieviel Code ist über Tests abgedeckt) zu sehen, folgenden Befehl ausführen, während das Virtual Environment aktiviert
ist:

```shell
cd schiller-online
source venv/bin/activate 
pytest --cov=src tests/ 
```

Die Tests unter [tests/](../tests/) sind in Ordner aufgeteilt die über Pytest auch separat aufgerufen werden können:

* [`unit/`](../tests/unit/) sind Tests die isoliert einzelne Funktionen in Modulen testen
* [`functional/`](../tests/functional/) sind Tests die die gesamte Applikation testen

"Fixtures" die für alle Tests gelten sollen stehen in der Konfigurationsdatei [conftest.py](../tests/conftest.py).

## Links
[Einstieg in Flask mit Pytest](https://www.patricksoftwareblog.com/unit-testing-a-flask-application/) \
[Übersicht zu Flask Contexts (Application/Request) für Testing](https://diegoquintanav.github.io/flask-contexts.html)

## Automated Testing / CI
Wir verwenden Github Actions, um bei jedem Push automatisch die Test Suite laufen zu lassen. Die "Workflows" dafür
finden sich in [`.github`](../.github/workflows/).
Hier das Ergebnis des letzten Commits:

[![All Tests](https://github.com/Oberschule-an-der-Egge/schiller-online/actions/workflows/all_tests.yml/badge.svg)](https://github.com/Oberschule-an-der-Egge/schiller-online/actions)

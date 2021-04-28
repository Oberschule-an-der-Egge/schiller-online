"""
Diese Datei ist der Startpunkt für uWSGI.
Ankommende HTTPS-Requests werden vom Webserver (z.B. nginx) an den laufenden Applikations-Server (uwsgi) weitergereicht,
der die Applikation (Schiller-Online) aufruft, um sie zu verarbeiten.
"""

# Callable for uWSGI
from src.main import create_app

application = create_app()

if __name__ == '__main__':
    application.run('0.0.0.0', port=5000, debug=True)

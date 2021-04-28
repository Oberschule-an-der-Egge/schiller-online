import os

from flask import Flask, render_template

from src.models import lookup_tables


def create_app():

    app = Flask(__name__)

    if os.environ.get('FLASK_ENV') == 'development':
        app.config.from_object('src.config.development')
    else:
        app.config.from_object('src.config.production')

    from src.views import routes
    app.register_blueprint(routes.bp)

    @app.before_first_request
    def initialise_redis_once():
        """Initialise redis with lookup tables
        """
        lookup_tables.feld_fach()
        lookup_tables.fach_feld()
        lookup_tables.fach_short_long()
        lookup_tables.possiblepruefung_filter_special()

    @app.errorhandler(503)
    def custom503(error):
        # response = error.description
        return render_template('error503.html')

    return app

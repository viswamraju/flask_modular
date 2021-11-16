# Imports from Flask
from flask import Flask
# Extension for implementing Alembic database migrations
from flask_migrate import Migrate
# Extension for implementing SQLAlchemy ORM
from flask_sqlalchemy import SQLAlchemy
# Extension for implementing Flask-Login for authentication
from flask_login import LoginManager
# Extension for implementing translations
from flask_babel import Babel
from flask_babel import lazy_gettext as _l
# Other imports
import os
import config

basedir = os.path.abspath(os.path.dirname(__file__))

db = SQLAlchemy()
babel = Babel()
login_manager = LoginManager()

def create_app(config_env=""):
    app = Flask(__name__)
    if not config_env:
        config_env = app.env
    app.config.from_object("config.{}Config".format(config_env.capitalize()))

    # Initializing extensions
    db.init_app(app)
    babel.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    login_manager.session_protection = "strong"
    login_manager.login_message = _l("You need to be logged in to access this page.")
    login_manager.login_message_category = "danger"

    # Imports from subpackages (views)
    with app.app_context():
        from app.album.views import album
        app.register_blueprint(album, url_prefix="/album")
        from app.main.views import main
        app.register_blueprint(main)
    from app.tour.views import tour
    app.register_blueprint(tour, url_prefix="/tour")
    from app.auth.views import auth
    app.register_blueprint(auth)

    from app.main.views import page_not_found
    app.register_error_handler(404, page_not_found)

    return app

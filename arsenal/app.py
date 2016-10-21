"""arsenal.app - application factory"""

from flask import Flask
from flask_gravatar import Gravatar
from flask_moment import Moment
from flask_pure import Pure
from flask_simplemde import SimpleMDE
from .forum import forum
from .user import user, init_app as user_init_app
from .models import init_app as models_init_app


def create_app(config_filename):
    """application factory"""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile(config_filename)
    models_init_app(app)
    user_init_app(app)
    Gravatar(app, default='identicon')
    Moment(app)
    Pure(app)
    SimpleMDE(app)
    app.register_blueprint(forum, url_prefix='/t')
    app.register_blueprint(user, url_prefix='/u')
    return app

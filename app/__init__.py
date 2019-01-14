# app/__init__.py

# third-party imports
from flask import Flask, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_admin import Admin

import os
import collections


# local imports
from config import app_config

# db variable initialization
db = SQLAlchemy()

# Login manager
login_manager = LoginManager()

# Flask admin
admin = Admin(name='FX REC', template_mode='bootstrap3')


def add_models_to_admin():
    from flask_admin.contrib.sqla import ModelView
    from app.models import Role, Privilege, Group
    admin.add_view(ModelView(Role, db.session))
    admin.add_view(ModelView(Privilege, db.session))
    admin.add_view(ModelView(Group, db.session))


def main_nav(active):
    Nav = collections.namedtuple('Nav', 'name path active')
    list = [
        Nav(name='Home', path='/', active=active == 'Home'),
        Nav(name='Members', path='/members', active=active == 'Members'),
        Nav(name='Contributions', path='/contributions',
            active=active == 'Contributions'),
        Nav(name='Roles',
            path='/roles', active=active == 'Roles')
    ]
    return list


def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SESSION_TYPE'] = 'filesystem'
    app.debug = True

    @app.context_processor
    def override_url_for():
        return dict(url_for=dated_url_for)

    def dated_url_for(endpoint, **values):
        if endpoint == 'static':
            filename = values.get('filename', None)
            if filename:
                file_path = os.path.join(app.root_path,
                                         endpoint, filename)
                values['q'] = int(os.stat(file_path).st_mtime)
        return url_for(endpoint, **values)

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "users.login"

    @login_manager.user_loader
    def load_user(user_id):
        from app.models import User
        user = User.get()
        return user

    '''
    Copyright current year
    '''
    @app.context_processor
    def inject_cpyear():
        from datetime import datetime
        return {'copyright_year': datetime.now().year}

    '''
    Flask admin
    '''
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    admin.init_app(app)
    add_models_to_admin()

    migrate = Migrate(app, db)
    from app import models
    from app import users

    from .members import members as members_blueprint
    app.register_blueprint(members_blueprint, url_prefix='/members')

    from .contributions import contributions as contributions_blueprint
    app.register_blueprint(contributions_blueprint,
                           url_prefix='/contributions')

    from .groups import groups as groups_blueprint
    app.register_blueprint(groups_blueprint,
                           url_prefix='/groups')

    from .users import users as users_blueprint
    app.register_blueprint(users_blueprint,
                           url_prefix='/users')

    '''
    from .privileges import privileges as privileges_blueprint
    app.register_blueprint(privileges_blueprint,
                           url_prefix='/privileges')
    '''

    from .roles import roles as roles_blueprint
    app.register_blueprint(roles_blueprint,
                           url_prefix='/roles')

    from .home import home as home_blueprint
    app.register_blueprint(home_blueprint)

    return app

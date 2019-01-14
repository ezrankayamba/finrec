# app/admin/__init__.py


from flask import Blueprint


def import_views():
    from . import views


home = Blueprint('home', __name__)
import_views()

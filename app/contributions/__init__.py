# app/contributions/__init__.py

from flask import Blueprint


def import_views():
    from . import views


contributions = Blueprint('contributions', __name__)
import_views()

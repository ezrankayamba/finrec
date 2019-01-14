# app/admin/__init__.py

from flask import Blueprint


def import_views():
    from . import views
    from app import models


roles = Blueprint('roles', __name__)
import_views()

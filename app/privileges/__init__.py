# app/admin/__init__.py

from flask import Blueprint


def import_views():
    from . import views
    from app import models


privileges = Blueprint('privileges', __name__)
import_views()

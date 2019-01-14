# app/home/views.py

from flask import render_template, flash
from app import main_nav
from . import home
from flask_login import login_required


@home.route('/')
def index():
    """
    Render the homepage template on the / route
    """
    navs = main_nav('Home')
    return render_template('home/index.html', navs=navs, title="Home")


@home.route('/dashboard')
def dashboard():
    """
    Render the dashboard template on the /dashboard route
    """
    return render_template('home/dashboard.html', title="Dashboard")

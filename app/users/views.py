# app/home/views.py

from flask import render_template, request, redirect, session, url_for, flash
from app import main_nav, db, login_manager
from . import users
from app.models import User
from sqlalchemy import text
from flask_login import current_user, login_user, login_required, logout_user
import requests
import json


@users.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        data = request.form
        username = data['username']
        password = data['password']
        resp = User.signup_user(username, password)
        if resp.ok:
            return redirect(url_for('users.login'))
        flash('Registration failed. Try again')
    return render_template('users/signup.html', navs=[])


@users.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home.index'))
    if request.method == 'POST':
        data = request.form
        username = data['username']
        password = data['password']
        resp = User.login_user(username, password)
        if resp.ok:
            res_data = json.loads(resp.text)
            access_token = res_data['access_token']
            refresh_token = res_data['refresh_token']
            session['access_token'] = access_token
            session['refresh_token'] = refresh_token
            user = User.get()
            result = login_user(user)
            next = request.args.get('next')
            flash('You are successfully logged in')
            return redirect(next or url_for('home.index'))
        flash('Login failed, try again using correct credentials')
    next = request.args.get('next')
    return render_template('users/login.html', navs=[], title="Login")


@users.route('/changepwd', methods=['GET', 'POST'])
@login_required
def changepwd():
    if request.method == 'POST':
        data = request.form
        username = data['username']
        password = data['password']
        resp = User.change_pwd(username, password)
        print('Change pwd response: ', resp.text)
        if resp.ok:
            flash('You are successfully changed password')
            return logout()
    return render_template('users/changepwd.html', navs=[])


@users.route('/logout', methods=['GET'])
@login_required
def logout():
    User.logout_user()
    logout_user()
    flash('You are successfully logged out')
    return redirect(url_for('home.index'))

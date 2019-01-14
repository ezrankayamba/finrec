# app/home/views.py

from flask import render_template, request, redirect, session
from app import main_nav, db
from . import privileges
from app.models import Privilege
from sqlalchemy import text
from flask_login import login_required, current_user


@privileges.route('/')
@login_required
def index():
    navs = main_nav('Privileges')
    q = request.args.get('q')
    if not q:
        privileges = Privilege.query.all()
    else:
        privileges = Privilege.query.filter(Privilege.name.like('%'+q+'%'))
    return render_template('privileges/index.html', privileges=privileges, navs=navs, title="Privileges")


@privileges.route('/manage', methods=['GET', 'POST'])
@privileges.route('/manage/<id>', methods=['GET', 'POST'])
@login_required
def manage(id=None):
    navs = main_nav('Privileges')
    if request.method == 'POST':
        data = request.form
        id = data['id']
        if id:
            m = Privilege.query.get(id)
            m.name = data['name']
        else:
            m = Privilege(name=data['name'])
            db.session.add(m)
        db.session.commit()
        return redirect("/privileges", code=302)
    else:
        privilege = None
        if id:
            privilege = Privilege.query.get(id)
        return render_template('privileges/manage.html', navs=navs, title="Privileges", privilege=privilege)


@privileges.route('/delete/<id>')
@login_required
def delete(id=None):
    m = Privilege.query.get(id)
    db.session.delete(m)
    db.session.commit()
    return redirect("/privileges", code=302)


@privileges.route('/deleteall')
@login_required
def deleteall():
    # Delete all here
    return redirect("/privileges", code=302)

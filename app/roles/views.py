# app/home/views.py

from flask import render_template, request, redirect, session, flash
from app import main_nav, db
from . import roles
from app.models import Role, RolePrivilege as RP, Privilege
from sqlalchemy import text
from flask_login import login_required, current_user


@roles.route('/')
@login_required
def index():
    navs = main_nav('Roles')
    q = request.args.get('q')
    if not q:
        roles = Role.query.all()
    else:
        roles = Role.query.filter(Role.name.like('%'+q+'%'))
    return render_template('roles/index.html', roles=roles, navs=navs)


@roles.route('/matrix', methods=['POST'])
@roles.route('/matrix/<id>', methods=['GET'])
@login_required
def matrix(id=None):
    navs = main_nav('Roles')
    if request.method == 'POST':
        data = request.form
        id = data['id']
        privileges = data['privileges']
        print(privileges)
        RP.query.filter(RP.role_id == id).delete()
        db.session.commit()
        for p in privileges:
            new_rp = RP(role_id=id, privilege_id=p)
            db.session.add(new_rp)
        db.session.commit()
        flash('Role matrix updated successfully')
        return redirect("/roles", code=302)
    else:
        role = None
        if id:
            role = Role.query.get(id)
        privileges = Privilege.query.all()
        return render_template('roles/matrix.html', navs=navs, role=role, privileges=privileges)


@roles.route('/manage', methods=['GET', 'POST'])
@roles.route('/manage/<id>', methods=['GET', 'POST'])
@login_required
def manage(id=None):
    navs = main_nav('Roles')
    if request.method == 'POST':
        data = request.form
        id = data['id']
        if id:
            m = Role.query.get(id)
            m.name = data['name']
        else:
            m = Role(name=data['name'])
            db.session.add(m)
        db.session.commit()
        return redirect("/roles", code=302)
    else:
        role = None
        if id:
            role = Role.query.get(id)
        return render_template('roles/manage.html', navs=navs, role=role)


@roles.route('/delete/<id>')
@login_required
def delete(id=None):
    m = Role.query.get(id)
    db.session.delete(m)
    db.session.commit()
    return redirect("/roles", code=302)


@roles.route('/deleteall')
@login_required
def deleteall():
    # Delete all here
    return redirect("/roles", code=302)

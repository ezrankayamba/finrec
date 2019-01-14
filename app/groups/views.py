# app/home/views.py

from flask import render_template, request, redirect, session
from app import main_nav, db
from . import groups
from app.models import Group
from sqlalchemy import text
from flask_login import login_required, current_user


@groups.route('/')
@login_required
def index():
    print('Current User after login: ', current_user)
    navs = main_nav('Groups')
    q = request.args.get('q')
    if not q:
        groups = Group.query.all()
    else:
        groups = Group.query.filter(Group.name.like('%'+q+'%'))
    msg = session.get('msg')
    session['msg'] = None
    return render_template('groups/index.html', groups=groups, navs=navs, title="Groups", msg=msg)


@groups.route('/manage', methods=['GET', 'POST'])
@groups.route('/manage/<id>', methods=['GET', 'POST'])
@login_required
def manage(id=None):
    navs = main_nav('Groups')
    if request.method == 'POST':
        data = request.form
        id = data['id']
        parent_id = data['parent_id']
        if id:
            m = Group.query.get(id)
            m.name = data['name']
            if parent_id:
                m.parent_id = parent_id
        else:
            m = Group(name=data['name'])
            if parent_id:
                m.parent_id = parent_id
            db.session.add(m)
        db.session.commit()
        return redirect("/groups", code=302)
    else:
        group = None
        if id:
            group = Group.query.get(id)
        groups = Group.query.all()
        return render_template('groups/manage.html', navs=navs, title="Groups", group=group, groups=groups)


@groups.route('/delete/<id>')
@login_required
def delete(id=None):
    m = Group.query.get(id)
    db.session.delete(m)
    db.session.commit()
    session['msg'] = 'Successfully deleted a group'
    return redirect("/groups", code=302)

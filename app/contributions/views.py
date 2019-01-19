# app/home/views.py

from flask import render_template, request, redirect, session
from app import main_nav, db
from . import contributions
from app.models import Contribution, Group
from flask_login import login_required


@contributions.route('/')
@login_required
def index():
    navs = main_nav('Contributions')
    q = request.args.get('q')
    if not q:
        contrs = Contribution.query.all()
    else:
        contrs = Contribution.query.filter(Contribution.name.like('%'+q+'%'))
    msg = session.get('msg')
    session['msg'] = None
    return render_template('contributions/index.html', contrs=contrs, navs=navs, title="Contributions", msg=msg)


@contributions.route('/manage', methods=['GET', 'POST'])
@contributions.route('/manage/<id>', methods=['GET', 'POST'])
@login_required
def manage(id=None):
    if request.method == 'POST':
        data = request.form
        id = data['id']
        if id:
            m = Contribution.query.get(id)
            m.name = data['name']
            m.price = data['price']
            m.group_id = data['group_id']
            # db.session.update(m)
        else:
            m = Contribution(name=data['name'], price=data['price'])
            db.session.add(m)
        db.session.commit()
        return redirect("/contributions", code=302)
    else:
        navs = main_nav('Contributions')
        groups = Group.query.all()
        contr = None
        if id:
            contr = Contribution.query.get(id)
        return render_template('contributions/manage.html', navs=navs, title="Contributions", contr=contr, groups=groups)


@contributions.route('/delete', methods=['GET'])
@login_required
def delete(action=None, id=None):
    m = Contribution.query.get(id)
    db.session.delete(m)
    db.session.commit()
    session['msg'] = 'Successfully deleted a contribution'
    return redirect("/contributions", code=302)

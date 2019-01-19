# app/home/views.py

from flask import render_template, request, redirect, session
from app import main_nav, db
from . import members
from app.models import Member, Payment, Contribution
from sqlalchemy import text
from flask_login import login_required


@members.route('/')
@login_required
def index():
    navs = main_nav('Members')
    q = request.args.get('q')
    if not q:
        members = Member.query.all()
    else:
        members = Member.query.filter(Member.name.like('%'+q+'%'))
    msg = session.get('msg')
    session['msg'] = None
    return render_template('members/index.html', members=members, navs=navs, title="Members", msg=msg)


def into_list(res):
    return [r for r in res]


def pending_list(id):
    sql = text(
        'select * from  vw_member_contributions where member_id = :member_id and (pending =1 or pending is null) order by last_update desc')
    return into_list(db.engine.execute(sql, {'member_id': id}))


def recent_list(id):
    sql = text(
        'select c.*, p.amount, p.record_date as pay_date from tbl_payment p left join tbl_contribution c on p.contribution_id = c.id where p.member_id = :member_id order by p.record_date desc limit 3')
    return into_list(db.engine.execute(sql, {'member_id': id}))


def eligible_roles():
    sql = text(
        'select r.* from tbl_role r')
    return into_list(db.engine.execute(sql, {}))


def eligible_groups():
    sql = text(
        'select g.* from tbl_group g order by g.name asc')
    return into_list(db.engine.execute(sql, {}))


@members.route('/payments/<id>', methods=['GET', 'POST'])
@login_required
def payments(id=None):
    navs = main_nav('Members')
    if request.method == 'POST':
        data = request.form
        m = Payment(member_id=data['member_id'],
                    contribution_id=data['contribution_id'], amount=data['amount'])
        db.session.add(m)
        db.session.commit()
        return redirect('/members/payments/{}'.format(id), code=302)
    else:
        member = Member.query.get(id)
        pending = pending_list(id)

        balance = 0
        for pc in pending:
            balance += pc.balance or pc.price
        recent = recent_list(id)
        print('Pending: ', pending)
        return render_template('members/payments.html', navs=navs, title="Members", member=member, pending=pending, recent=recent, balance=balance)


@members.route('/manage', methods=['GET', 'POST'])
@members.route('/manage/<id>', methods=['GET', 'POST'])
@login_required
def manage(id=None):
    navs = main_nav('Members')
    if request.method == 'POST':
        data = request.form
        id = data['id']
        if id:
            m = Member.query.get(id)
            m.name = data['name']
            m.group_id = data['group_id']
            # db.session.update(m)
        else:
            m = Member(name=data['name'])
            m.group_id = data['group_id']
            db.session.add(m)
        db.session.commit()
        return redirect("/members", code=302)
    else:
        groups = eligible_groups()
        member = None
        if id:
            member = Member.query.get(id)
        return render_template('members/manage.html', navs=navs, title="Members", member=member, groups=groups)


@members.route('/role/<id>', methods=['GET', 'POST'])
@login_required
def role(id=None):
    navs = main_nav('Members')
    if request.method == 'POST':
        data = request.form
        id = data['id']
        if id:
            m = Member.query.get(id)
            m.role_id = data['role_id']
            m.username = data['username']
        db.session.commit()
        return redirect("/members", code=302)
    else:
        roles = eligible_roles()
        member = None
        if id:
            member = Member.query.get(id)
        return render_template('members/role.html', navs=navs, title="Members", member=member, roles=roles)


@members.route('/delete/<id>')
@login_required
def delete(id=None):
    m = Member.query.get(id)
    db.session.delete(m)
    db.session.commit()
    session['msg'] = 'Successfully deleted a member'
    return redirect("/members", code=302)

# app/models.py

from flask import session
import requests
import json
import os
from app import db

# auth_base_url = 'http://35.196.97.23:6001'
auth_base_url = os.getenv('CENTRI_JWT_BASE_URL')


def get_user():
    access_token = session['access_token']
    if not access_token:
        return None
    resp = requests.get('{}/user'.format(auth_base_url),
                        headers={'Authorization': 'Bearer {}'.format(access_token)})
    res_data = json.loads(resp.text)
    if 'logged_in_as' not in res_data:
        # Expired access token, try refresh
        print('Msg: ', res_data['msg'])
        refresh_token = session['refresh_token']
        resp = requests.get('{}/token/refresh'.format(auth_base_url),
                            headers={'Authorization': 'Bearer {}'.format(access_token)})
        res_data = json.loads(resp.text)
        if 'access_token' not in res_data:
            # Exired refresh token, login
            print('Msg: ', res_data['msg'])
            return None
        # Got new token
        access_token = res_data['access_token']
        session['access_token'] = access_token
        return get_user()
    user = res_data['logged_in_as']
    username = user['username']
    print('User.get -> Username: ', username)
    return User(username)


class User(object):
    username = None

    def __init__(self, username):
        self.username = username

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.username)

    @classmethod
    def signup_user(cls, username, password):
        cred = {"username": username, "password": password}
        return requests.post('{}/registration'.format(auth_base_url), json=cred)

    @classmethod
    def change_pwd(cls, username, password):
        access_token = session['access_token']
        cred = {"username": username, "password": password}
        return requests.post('{}/changepwd'.format(auth_base_url), json=cred, headers={'Authorization': 'Bearer {}'.format(access_token)})

    @classmethod
    def login_user(cls, username, password):
        cred = {"username": username, "password": password}
        return requests.post('{}/login'.format(auth_base_url), json=cred)

    @classmethod
    def logout_user(cls):
        access_token = session['access_token']
        requests.post('{}/logout/access'.format(auth_base_url),
                      headers={'Authorization': 'Bearer {}'.format(access_token)})
        refresh_token = session['refresh_token']
        requests.post('{}/logout/refresh'.format(auth_base_url),
                      headers={'Authorization': 'Bearer {}'.format(refresh_token)})

    @classmethod
    def get(cls, user_id=None):
        token = session['access_token']
        if not token:
            return None
        resp = requests.get('{}/user'.format(auth_base_url),
                            headers={'Authorization': 'Bearer {}'.format(token)})
        print('Response: ', resp.text)
        res_data = json.loads(resp.text)
        if 'logged_in_as' not in res_data:
            return None
        user = res_data['logged_in_as']
        username = user['username']
        print('User.get -> Username: ', username)
        return User(username)

    def __repr__(self):
        return '<User: {0}>'.format(self.username)


class Group(db.Model):
    __tablename__ = 'tbl_group'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    record_date = db.Column(db.DateTime(timezone=True))
    last_update = db.Column(db.DateTime(timezone=True))
    parent_id = db.Column(db.Integer, db.ForeignKey(
        'tbl_group.id'), nullable=True)
    parent = db.relationship("Group", remote_side=[id])
    members = db.relationship(
        'Member', lazy='select', backref=db.backref('tbl_member', lazy='joined'))

    def __repr__(self):
        return '{}'.format(self.name)


class Privilege(db.Model):
    __tablename__ = 'tbl_privilege'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    record_date = db.Column(db.DateTime(timezone=True))
    last_update = db.Column(db.DateTime(timezone=True))

    def __repr__(self):
        return '{}'.format(self.name)


class RolePrivilege(db.Model):
    __tablename__ = 'tbl_role_privilege'
    id = db.Column(db.Integer, primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey(
        'tbl_role.id'), nullable=False)
    privilege_id = db.Column(db.Integer, db.ForeignKey(
        'tbl_privilege.id'), nullable=False)
    record_date = db.Column(db.DateTime(timezone=True))
    last_update = db.Column(db.DateTime(timezone=True))
    privilege = db.relationship("Privilege")

    def __repr__(self):
        return '{}'.format(self.name)


class Role(db.Model):
    __tablename__ = 'tbl_role'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    record_date = db.Column(db.DateTime(timezone=True))
    last_update = db.Column(db.DateTime(timezone=True))
    privileges = db.relationship('RolePrivilege', lazy='select')

    def __repr__(self):
        return '{}'.format(self.name)


class Member(db.Model):
    __tablename__ = 'tbl_member'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    record_date = db.Column(db.DateTime(timezone=True))
    last_update = db.Column(db.DateTime(timezone=True))
    group_id = db.Column(db.Integer, db.ForeignKey('tbl_group.id'))
    group = db.relationship(Group, backref='tbl_member')
    role_id = db.Column(db.Integer, db.ForeignKey('tbl_role.id'))
    role = db.relationship(Role, backref='tbl_member')
    payments = db.relationship(
        'Payment', lazy='select', backref=db.backref('tbl_payment', lazy='joined'))

    def __repr__(self):
        return 'Member: {}'.format(self.name)


class Contribution(db.Model):
    __tablename__ = 'tbl_contribution'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    record_date = db.Column(db.DateTime(timezone=True))
    last_update = db.Column(db.DateTime(timezone=True))

    def __repr__(self):
        return 'Contribution: {} - Tsh: {}'.format(self.name, self.price)


class Payment(db.Model):
    __tablename__ = 'tbl_payment'
    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey(
        'tbl_member.id'), nullable=False, )
    contribution_id = db.Column(db.Integer, db.ForeignKey(
        'tbl_contribution.id'), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    record_date = db.Column(db.DateTime(timezone=True))
    last_update = db.Column(db.DateTime(timezone=True))

    def __repr__(self):
        return 'Contribution: {} - Tsh: {}'.format(self.member_id, self.amount)

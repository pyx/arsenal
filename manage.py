#!/usr/bin/env python
# -*- coding: utf-8 -*-
from getpass import getpass
from flask_script import Manager

from arsenal.app import create_app
from arsenal.models import Post, Topic, User, db

app = create_app('config.py')
manager = Manager(app)

try:
    get_input = raw_input
except NameError:
    get_input = input


@manager.shell
def make_shell_context():
    return dict(Post=Post, Topic=Topic, User=User, db=db)


@manager.command
def init_db():
    """Create databse"""
    db.create_all()


@manager.command
def passwd(email=None):
    """Change user password"""
    while not email:
        email = get_input('Please enter email as user name: ')
    newpass = getpass('Please enter password for {}: '.format(email))
    confirm = getpass('Please enter password for {} again: '.format(email))
    if not newpass:
        print('Empty password, nothing change.')
        return
    if newpass != confirm:
        print('Please enter the same password.')
        return
    user = User.query.filter_by(email=email).one_or_none()
    if not user:
        user = User(email=email, password=newpass)
        user.name = email
        print('new user created')
    else:
        user.password = newpass
    db.session.add(user)
    db.session.commit()


if __name__ == '__main__':
    manager.run()

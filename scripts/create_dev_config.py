#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

DEV_CONFIG_TEMPLATE = """# local development configuration file
DEBUG = True
SECRET_KEY = \"\"\"
{}
\"\"\"
SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = True
"""
DEV_CONFIG = 'instance/config.py'


def create_dev_config():
    """creates local development configuration file"""
    if not os.path.exists(DEV_CONFIG):
        try:
            os.mkdir('instance')
        except OSError:
            print('already exists')
            pass
        with open(DEV_CONFIG, 'w') as config:
            config.write(DEV_CONFIG_TEMPLATE.format(os.urandom(20)))


if __name__ == '__main__':
    create_dev_config()

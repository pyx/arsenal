from fabric.api import cd, env, hosts, local, run, sudo

env.user = 'APP_USER'
env.hosts = ['APP_HOST']

DEPLOY_TARGET = 'APP_DEPLOY_PATH'


def passwd(username):
    with cd(DEPLOY_TARGET):
        run('VIRTUALENV_PATH/bin/python manage.py passwd {}'.format(username))


def restart():
    sudo('service arsenal restart')
    sudo('service nginx restart')


def upload():
    local('hg push deploy')
    with cd(DEPLOY_TARGET):
        run('hg up')


def deploy():
    upload()

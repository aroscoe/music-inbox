from __future__ import with_statement

from fabric.api import *

from local_settings import FABRIC_USER, FABRIC_HOSTS

env.user = FABRIC_USER     # user
env.hosts = FABRIC_HOSTS   # ['11.111.111.111']

def deploy():
    with cd('/home/musicinbox/music-inbox'):
        sudo('git pull', user='musicinbox')
        sudo('/home/musicinbox/.virtualenvs/music-inbox/bin/pip install -r REQUIREMENTS', user='musicinbox')
        run('/home/musicinbox/.virtualenvs/music-inbox/bin/python manage.py syncdb')
        run('rsync -a --delete assets /home/musicinbox/public/')
        run('chmod -R 755 /home/musicinbox/public')
        restart_uwsgi()

def restart_celery():
    run('supervisorctl restart celery celerybeat')

def restart_uwsgi():
    run('supervisorctl restart uwsgi:*')

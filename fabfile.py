from local_settings import FABRIC_USER, FABRIC_HOSTS

from fabric.api import *

env.user = FABRIC_USER     # user
env.hosts = FABRIC_HOSTS   # ['11.111.111.111']

def deploy():
    with cd('music-inbox'):
        run('git pull')
        run('~/.virtualenvs/music-inbox/bin/python manage.py syncdb')
        run('rsync -a --delete assets /public/music-inbox/')

def restart_celery():
    run('supervisorctl restart celery celerybeat')

def restart_uwsgi():
    run('supervisorctl restart uwsgi:*')

import os, sys

# redirect sys.stdout to sys.stderr for bad libraries like geopy that uses
# print statements for optional import exceptions.
sys.stdout = sys.stderr

from os.path import abspath, dirname, join
sys.path.insert(0, abspath(join(dirname(__file__), "../../")))

from django.conf import settings
os.environ['DJANGO_SETTINGS_MODULE'] = 'music-inbox.settings'

sys.path.insert(0, join(settings.PROJECT_ROOT, "libs"))
sys.path.insert(0, join(settings.PROJECT_ROOT, "apps"))

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

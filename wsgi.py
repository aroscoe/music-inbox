import os
import sys
from os.path import join
from django.conf import settings

# redirect sys.stdout to sys.stderr for bad libraries like geopy that uses
# print statements for optional import exceptions.
sys.stdout = sys.stderr

os.environ['DJANGO_SETTINGS_MODULE'] = 'music-inbox.settings'

sys.path.insert(0, join(settings.PROJECT_ROOT))
sys.path.insert(0, join(settings.PROJECT_ROOT, "libs"))
sys.path.insert(0, join(settings.PROJECT_ROOT, "apps"))

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

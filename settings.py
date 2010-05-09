# Django settings for music-inbox project.

import os.path
import logging
from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS

PROJECT_ROOT = os.path.realpath(os.path.dirname(__file__))

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DATABASE_ENGINE = 'sqlite3'    # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = 'dev.db'       # Or path to database file if using sqlite3.
DATABASE_USER = ''             # Not used with sqlite3.
DATABASE_PASSWORD = ''         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

# Celery settings
BROKER_HOST = "localhost"
BROKER_PORT = 5672
BROKER_USER = "musicinbox"
BROKER_PASSWORD = "musicinbox"
BROKER_VHOST = "musicinbox"

CELERY_DEFAULT_QUEUE = 'musicinbox_tasks'
CELERY_QUEUES = {
    'musicinbox_tasks': {'binding_key': 'task.#',},
    'musicbrainz_tasks': {'binding_key': 'musicbrainz.#',},
}
CELERY_DEFAULT_EXCHANGE = 'musicinbox'
CELERY_DEFAULT_EXCHANGE_TYPE = "topic"
CELERY_DEFAULT_ROUTING_KEY = "task.regular"
CELERYD_CONCURRENCY=4

# celerybeat settings
CELERYBEAT_LOG_FILE='/tmp/celerybeat.log'
CELERYBEAT_LOG_LEVEL=logging.INFO

CELERYD_LOG_FILE='/tmp/celeryd.log'
CELERYD_LOG_LEVEL='INFO'

AMAZON_KEY = ''
AMAZON_SECRET = ''
KEY = [1, 1, 1, 1]

TIME_ZONE = 'US/Eastern'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(PROJECT_ROOT, "assets")

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/assets/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/assets/admin/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '=cc+1ipy28ezwq9q$z0hm8)6i*wtfbqvj$-0!x4d*_-3i_rypz'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)

ROOT_URLCONF = 'music-inbox.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_ROOT, 'templates'),
)

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',

    'celery',
    'django_cron',
    'library',
    'api',
)

UPLOADS_DIR = os.path.join(PROJECT_ROOT, 'uploads/')

LOG_FILE = '/tmp/music-inbox-log'
LOG_LEVEL = logging.CRITICAL

# musicbrainz rate limiting
SLEEP_TIME = 2

# Local Settings
try:
    from local_settings import *
except ImportError:
    pass

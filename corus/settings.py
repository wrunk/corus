import os
import sys
from google.appengine.api import memcache
sys.modules['memcache'] = memcache
from google.appengine.api.app_identity import get_application_id


BASE_DIR = os.path.abspath(os.path.dirname(__file__)) + os.sep

print "Loading settings base dir (%s)" % BASE_DIR

DEBUG = True
TEMPLATE_DEBUG = DEBUG


# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Los_Angeles'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True


# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'


# Make this unique, and don't share it with anybody.
SECRET_KEY = '$2ighjfjhfoiu8uibkj;oike71a9dkt4c84fpa)4#q8#@&@1*g!'


ROOT_URLCONF = 'corus.urls'

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
)

INSTALLED_APPS = (
    # 'django.contrib.auth',
    # 'django.contrib.sessions',
    # 'django.contrib.messages',
    'django.contrib.sitemaps',
    'corus.console',
)

VERSION_ID = os.environ.get("CURRENT_VERSION_ID", 'local')

SERVER_SOFTWARE = os.environ.get('SERVER_SOFTWARE', 'Dev')

VERSION_NAME = os.environ.get("CURRENT_VERSION_ID", 'local').split('.')[0]

APPLICATION_NAME = get_application_id()

if not 'Dev' in SERVER_SOFTWARE:
    # production deploy settings
    pass

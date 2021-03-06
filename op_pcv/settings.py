# Django settings for op_pcv project.

import os
import logging
import django.conf.global_settings as DEFAULT_SETTINGS

import environ
root = environ.Path(__file__) - 2  # three folder back (/a/b/c/ - 3 = /)

# set default values and casting
env = environ.Env(
    DEBUG=(bool, False),
    TEMPLATE_DEBUG=(bool, True),
)
env.read_env(root('.env'))

DEBUG = env('DEBUG')
TEMPLATE_DEBUG = env('TEMPLATE_DEBUG')


DATABASES = {
    'default': env.db(),  # Raises ImproperlyConfigured exception if DATABASE_URL not in os.environ
}

# rss feeds for openpolis blog, twitter account and facebook page
OP_BLOG_FEED = "http://blog.openpolis.it/categorie/parlamentocasadivetro/feed/"
OP_BLOG_PCV_TAG = "parlamentocasadivetro"
OP_BLOG_PCV_CATEGORY = "ParlamentoCasadiVetro"
# caches the last blog post about PCV for 1min
# OP_BLOG_CACHETIME = 60

MEDIA_ROOT = root('assets')
MEDIA_URL = '/media/'
STATIC_ROOT = root('static')
STATIC_URL = '/static/'

SECRET_KEY = env('SECRET_KEY') # Raises ImproperlyConfigured exception if SECRET_KEY not in os.environ

REPO_ROOT = root()
PROJECT_ROOT = root('op_pcv')

ADMINS = ()
MANAGERS = ADMINS


# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ['localhost', 'parlamentocasadivetro.openpolis.it']

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Europe/Rome'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'it-IT'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True



# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)


# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'op_pcv.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'op_pcv.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    "templates/"
)

TEMPLATE_CONTEXT_PROCESSORS = DEFAULT_SETTINGS.TEMPLATE_CONTEXT_PROCESSORS + (
    'op_pcv.context_processor.main_settings',
    'django.core.context_processors.request',
)



INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    'op_pcv',
    'django_extensions',
    'south',

)

#CACHES = {
#    'default': {
#        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
#        'LOCATION': '127.0.0.1:11211',
#        }
#}

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt' : "%d/%b/%Y %H:%M:%S"
        },
        },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'console':{
            'level':'DEBUG',
            'class':'logging.StreamHandler',
            'formatter': 'standard'
        },
        'logfile': {
            'level':'INFO',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': REPO_ROOT + "/log/logfile",
            'maxBytes': 10000000,
            'backupCount': 10,
            'formatter': 'standard',
            },
        'feedlogfile': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'mode': 'a',
            'filename': REPO_ROOT + "/log/feedlog.log",
            'formatter': 'standard',
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
            },
        'csvimport': {
            'handlers': ['console', 'logfile'],
            'encoding': 'UTF-8',
            'level': 'DEBUG',
            'propagate': True,
            },
        'feed': {
            'handlers': ['feedlogfile'],
            'level': 'DEBUG',
            'encoding': 'UTF-8',
            'propagate': True,
        },
    }
}

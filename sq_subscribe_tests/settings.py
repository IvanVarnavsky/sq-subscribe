# -*- coding: utf-8 -*-
import os
import djcelery

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = ()

MANAGERS = ADMINS


PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'sqlite.db',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

TIME_ZONE = 'Europe/Moscow'

LANGUAGE_CODE = 'ru-RU'

SITE_ID = 1

USE_I18N = True

USE_L10N = True

MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media/')

MEDIA_URL = '/media/'

STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static/')

STATIC_URL = '/static/'

STATICFILES_DIRS = ()

ADMIN_MEDIA_PREFIX = STATIC_URL + "admin/"


STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

SECRET_KEY = 's+m51jp(bx380!u#0f8owd-(n6_))%-332r1xg6z14)@_w+7c3'

# Расширенный пользователь
AUTHENTICATION_BACKENDS = (
    'sq_core.baseuser.backends.CustomUserModelBackend',
)
CUSTOM_USER_MODEL = 'user.User'


TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_ROOT, 'templates')
)



djcelery.setup_loader()

CELERY_RESULT_BACKEND = "mongodb"
CELERY_MONGODB_BACKEND_SETTINGS = {
    "host": "127.0.0.1",
    "port": 27017,
    "database": "celery",
    "taskmeta_collection": "subscribes_meta"
}

BROKER_BACKEND = "mongodb"
BROKER_HOST = "localhost"
BROKER_PORT = 27017
BROKER_USER = ""
BROKER_PASSWORD = ""
BROKER_VHOST = "celery"

CELERYBEAT_SCHEDULER = "djcelery.schedulers.DatabaseScheduler"

CELERY_SEND_TASK_ERROR_EMAILS = True
#CELERY_IMPORTS = ('sq_subscribe.subscribe.tasks', )

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'sq_core',
    'sq_core.basemodel',
    'sq_widgets',
    'user',
    'djcelery',
    'sq_subscribe',
    'sq_subscribe.subscribe',
    'sq_subscribe.mailqueue',
    'simplemodel',

)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.request',

)


EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'kexbit@gmail.com'
EMAIL_HOST_PASSWORD = 'dav200588'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
SERVER_EMAIL = EMAIL_HOST_USER
DEFAULT_FROM_EMAIL = 'SevenQuark.com <noreply@SevenQuark.com>'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_TEMPLATE_DIR = 'email'
SEND_MAILQUEUE_DELAY = 60 * 2
SUBSCRIBED_MODELS = ('simplemodel.SimpleModel',)
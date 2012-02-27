# -*- coding: utf-8 -*-
import os

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = ()

MANAGERS = ADMINS


PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))

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
    os.path.join(PROJECT_ROOT, 'templates'),
)


INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'sq_admin',
    'sq_subscribe',
    'sq_subscribe.subscribe',#TODO Без этой поебени сельдерей не видит тасков, хз почему
    'user',
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

SUBSCRIBED_MODELS = ('simplemodel.SimpleModel',)

#ADMIN_SUBSCRIBE_TEMPLATE_DIR = 'email/admin'
#TODO настройки модулей джанги не засунуть в модуль по дефолту, т.к некоторые ее модули инициализируются до начала импорта настроек
EMAIL_HOST =  'smtp.gmail.com'
EMAIL_HOST_USER =  'kexbit@gmail.com'
EMAIL_HOST_PASSWORD = 'dav200588'
EMAIL_PORT =  587
EMAIL_USE_TLS = True
SERVER_EMAIL =  EMAIL_HOST_USER
DEFAULT_FROM_EMAIL =  'SevenQuark.com <noreply@SevenQuark.com>'
EMAIL_BACKEND =  'django.core.mail.backends.smtp.EmailBackend'
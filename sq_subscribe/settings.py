# -*- coding: utf-8 -*-

def inject_module_apps():
    from django.conf import settings
    APPS = [
        'sq_core',
        'sq_core.basemodel',
        'sq_widgets',
        'sq_tasks',
        'sq_subscribe.mailqueue',
        'sq_subscribe.subscribe',
    ]

    settings.INSTALLED_APPS = APPS + settings.INSTALLED_APPS
    return APPS


EMAIL_HOST =  'smtp.gmail.com'
EMAIL_HOST_USER =  'kexbit@gmail.com'
EMAIL_HOST_PASSWORD = 'dav200588'
EMAIL_PORT =  587
EMAIL_USE_TLS = True
SERVER_EMAIL =  EMAIL_HOST_USER
DEFAULT_FROM_EMAIL =  'SevenQuark.com <noreply@SevenQuark.com>'
EMAIL_BACKEND =  'django.core.mail.backends.smtp.EmailBackend'
EMAIL_TEMPLATE_DIR =  'email'
SEND_MAILQUEUE_DELAY =  30
SUBSCRIBED_MODELS =  ()
ADMIN_SUBSCRIBE_TEMPLATE_DIR = EMAIL_TEMPLATE_DIR

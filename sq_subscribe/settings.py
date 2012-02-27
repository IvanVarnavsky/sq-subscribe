# -*- coding: utf-8 -*-

def inject_module_apps():
    from django.conf import settings
    APPS = [
        'sq_core',
        'sq_core.basemodel',
        'sq_widgets',
        'sq_tasks',
        'sq_subscribe.subscribe',
        'sq_subscribe.mailqueue',
    ]

    settings.INSTALLED_APPS = APPS + settings.INSTALLED_APPS
    return APPS

EMAIL_TEMPLATE_DIR =  'email'
SUBSCRIBED_MODELS =  ()
ADMIN_SUBSCRIBE_TEMPLATE_DIR = EMAIL_TEMPLATE_DIR


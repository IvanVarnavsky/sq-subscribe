# -*- coding: utf-8 -*-
import os

def inject_module_apps():
    from django.conf import settings
    APPS = (
        'sq_core',
        'sq_user',
        'sq_widgets',
        'sq_tasks',
        'sq_subscribe.subscribe',
        'sq_subscribe.mailqueue',
    )
    return APPS

EMAIL_TEMPLATE_DIR =  'email'
SUBSCRIBED_MODELS =  ()
ADMIN_SUBSCRIBE_TEMPLATE_DIR = EMAIL_TEMPLATE_DIR

# путь до папки media, в общем случае она пуста в начале
MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media')
MEDIA_URL = '/media/'  # URL для медии в шаблонах
# -*- coding: utf-8 -*-
from django.conf import settings

def setup():
    # INSTALLED_APPS
    APPS = [
        'sq_core',
        'sq_core.basemodel',
        'sq_widgets',
        'sq_tasks',
        'sq_subscribe.subscribe',
        'sq_subscribe.mailqueue',
    ]

    settings.INSTALLED_APPS = APPS + settings.INSTALLED_APPS
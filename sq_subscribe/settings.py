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


from django.conf import settings
settings.EMAIL_HOST = getattr(settings, "EMAIL_HOST", 'smtp.gmail.com')
settings.EMAIL_HOST_USER = getattr(settings, "EMAIL_HOST_USER", 'kexbit@gmail.com')
settings.EMAIL_HOST_PASSWORD = getattr(settings, "EMAIL_HOST_PASSWORD", 'dav200588')
settings.EMAIL_PORT = getattr(settings, "EMAIL_PORT", 587)
settings.EMAIL_USE_TLS = getattr(settings, "EMAIL_USE_TLS", True)
settings.SERVER_EMAIL = getattr(settings, "SERVER_EMAIL", settings.EMAIL_HOST_USER)
settings.DEFAULT_FROM_EMAIL = getattr(settings, "DEFAULT_FROM_EMAIL", 'SevenQuark.com <noreply@SevenQuark.com>')
settings.EMAIL_BACKEND = getattr(settings, "EMAIL_BACKEND", 'django.core.mail.backends.smtp.EmailBackend')
settings.EMAIL_TEMPLATE_DIR = getattr(settings, "EMAIL_TEMPLATE_DIR", 'email')
settings.SEND_MAILQUEUE_DELAY = getattr(settings, "SEND_MAILQUEUE_DELAY", 30)
settings.SUBSCRIBED_MODELS = getattr(settings, "SUBSCRIBED_MODELS", ())
settings.ADMIN_SUBSCRIBE_TEMPLATE_DIR = getattr(settings, "ADMIN_SUBSCRIBE_TEMPLATE_DIR", settings.EMAIL_TEMPLATE_DIR)
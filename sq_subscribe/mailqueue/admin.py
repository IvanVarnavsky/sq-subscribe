from django.contrib import admin
from sq_subscribe.mailqueue.models import MailQueue

admin.site.register(MailQueue)

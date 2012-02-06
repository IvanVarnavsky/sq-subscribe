from django.contrib import admin
from sq_subscribe.sendmail.models import MailQueue

admin.site.register(MailQueue)

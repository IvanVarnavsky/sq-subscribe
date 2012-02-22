from datetime import datetime
import json
from celery.task import task
from django.conf import settings
from django.contrib.sites.models import Site
from django.core import serializers
from sq_subscribe.mailqueue.models import create_mailqueue
from sq_subscribe.mailqueue.tasks import send_concrete_mailqueue
from sq_subscribe.subscribe.models import Subscribe, UserSubscribes

@task
def build_subsribe_query(subscribe_id):
    try:
        subscribe = Subscribe.objects.get(pk = subscribe_id)
    except Exception:
        raise Exception('Subscribe not found')
    usersubscribes = UserSubscribes.objects.filter(subscribe = subscribe)
    subscribe.last_send_date = datetime.now()
    if usersubscribes.count() > 0:
        message = {'sitename': Site.objects.get(id=settings.SITE_ID).name}
        objects = subscribe.get_modelname().objects.all()
        data_objects = serializers.serialize("json", objects)
        message.update({'objects':json.loads(data_objects)})
        mail_ids = []
        for usersub in usersubscribes:
            data_user = {'unsubscribe':usersub.unsubscribe_link,'username':usersub.user.username}
            vars = message
            vars.update({'user':data_user})
            mail = create_mailqueue(subject=subscribe.subject,template=subscribe.message,send_to=usersub.user.email,
                             content_type=subscribe.content_type,message=vars)
            mail_ids.append(mail.id)
        send_concrete_mailqueue.delay(mail_ids)
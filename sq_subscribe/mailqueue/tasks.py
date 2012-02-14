from datetime import timedelta
import json
from celery.task import task, periodic_task
from django.core import mail
from sq_tasks.simpletask.decorators import simple_task
from sq_subscribe.mailqueue.models import MailQueue
from django.conf import settings

#TODO пофиксить генерацию кучи подписок.

#TODO непонятно, как лучше выполнять очередь:
# 1. Вызовом асинхронного таска из генерации подписки и передачей созданных подписок
# 2. Периодичный таск, раз в 2 минуты который отправляет по 100 подписок.
#TODO сделать независимую работу p_t и s_t
@periodic_task(name='send_mailqueue', run_every=getattr(settings, "SEND_MAILQUEUE_DELAY", 60*2))
#@simple_task(sleep = settings.SEND_MAILQUEUE_DELAY if settings.SEND_MAILQUEUE_DELAY else 60*2)
def send_mailqueue():
    emails = MailQueue.objects.all().order_by('created_date')[0:100]
    if len(emails) > 0:
        connection = None
        try:
            connection = mail.get_connection(fail_silently=True)
            connection.open()
            for email in emails:
                msg = email.send_email(connection)
                try:
                    msg.send()
                    pass
                except Exception:
                    raise('MESSAGE %s CAN NOT SENDED'%email.id)
        finally:
            connection.close()



@task(name='send_concrete_mailqueue',ignore_result=True)
def send_concrete_mailqueue(queue_ids):
    if len(queue_ids) > 0:
        connection = None
        try:
            connection = mail.get_connection(fail_silently=True)
            connection.open()
            for email_id in queue_ids:
                email = MailQueue.objects.get(pk=email_id)
                msg = email.send_email(connection)
                try:
                    msg.send()
                except Exception:
                    raise('MESSAGE %s CAN NOT SENDED'%email.id)
        finally:
            connection.close()


#Асинхронная отправка сообщения, подойдет для уведомлений.
@task(name='send_email_message')
def send_email_message(subject,template,send_to,content_type,message=None,send_from=None):
    from django.conf import settings
    if send_from is None:
        send_from = settings.DEFAULT_FROM_EMAIL
    msg = {"data":message}
    email = MailQueue.objects.create(message=json.dumps(msg),send_to=send_to,subject=subject,template=template,send_from=send_from,content_type=content_type)
    email.save()
    connection = None
    try:
        connection = mail.get_connection(fail_silently=True)
        connection.open()
        msg = email.send_email(connection)
        try:
            msg.send()
            email.delete()
        except Exception:
            raise('MESSAGE %s CAN NOT SENDED'%email.id)
    finally:
        connection.close()
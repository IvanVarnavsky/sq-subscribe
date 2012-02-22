import json
from celery.task import task
from django.core import mail
from sq_subscribe.mailqueue.models import MailQueue


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
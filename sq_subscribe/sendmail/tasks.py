from datetime import timedelta
import json
from celery.task import periodic_task, task
from django.core import mail
from sq_tasks.simpletask.decorators import simple_task
from sq_subscribe.sendmail.models import MailQueue
from django.conf import settings

@simple_task(sleep = settings.SEND_MAILQUEUE_DELAY if settings.SEND_MAILQUEUE_DELAY else 60*2)
@task(name='send_mailqueue',ignore_result=True, default_retry_delay=timedelta(seconds= settings.SEND_MAILQUEUE_DELAY if settings.SEND_MAILQUEUE_DELAY else 60*2))
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
                    email.delete()
                except Exception:
                    raise('MESSAGE %s CAN NOT SENDED'%email.id)
        finally:
            connection.close()

#Асинхронная отправка сообщения, подойдет для уведомлений.
@task(name='send_email_message')
def send_email_message(subject,template,send_to,content_type,message=None,send_from=None):
    print 'SEND_EMAIL_MESSAGE'
    from django.conf import settings
    if send_from is None:
        send_from = settings.DEFAULT_FROM_EMAIL
    msg = {"message":message}
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
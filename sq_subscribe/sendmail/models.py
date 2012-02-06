# -*- coding: utf-8 -*-
from datetime import datetime
from django.template.base import TemplateDoesNotExist
from django.utils import simplejson as json

from django.core.mail.message import EmailMultiAlternatives, EmailMessage
from django.db import models
from django.template.loader import render_to_string
from django.utils.html import strip_tags

CONTENT_TYPE = [
    ('html', u'В формате HTML'),
    ('plain', u'В текстовом формате'),
]

class MailQueue(models.Model):
    send_to = models.CharField(max_length=1000,null=False)
    send_from = models.EmailField(null=False)
    subject = models.CharField(max_length=1000,null=True,blank=True,default=u'Без темы')
    message = models.TextField()
    template = models.TextField(blank=True)
    created_date = models.DateTimeField(default=datetime.now())
    content_type = models.CharField(max_length=100, blank=True, choices=CONTENT_TYPE)

    def __unicode__(self):
        return u'Mail message ' + str(self.subject)

    class Meta:
        db_table = 'mailqueue'
        verbose_name = 'Письмо'
        verbose_name_plural = 'Письма'


    def send_email(self,connecion):
        vars = json.loads(self.message)
        from django.conf import settings
        template_directory = settings.EMAIL_TEMPLATE_DIR  if settings.EMAIL_TEMPLATE_DIR else 'email'
        #TODO сделать логику выбора рендера шаблона из файла или из базы
        try:
            html_content = render_to_string(template_directory+'/%s'%self.template,vars)
        except TemplateDoesNotExist:
            raise TemplateDoesNotExist('Template dir %s does not exist.'%template_directory)
        text_content = strip_tags(html_content)
        try:
            if self.content_type == 'html':
                msg = EmailMultiAlternatives(self.subject,text_content,from_email=self.send_from,to=[self.send_to],connection=connecion)
                msg.attach_alternative(html_content,"text/html")
            else :
                msg = EmailMessage(self.subject,text_content,from_email=self.send_from,to=[self.send_to],connection=connecion)
        except Exception:
            raise Exception('Email message %s can not created.'%self.id)
        return msg

def create_mailqueue(subject,template,send_to,content_type,message=None,send_from=None):
    from django.conf import settings
    if send_from is None:
        send_from = settings.DEFAULT_FROM_EMAIL
    msg = {"message":message}
    mail = MailQueue.objects.create(message=json.dumps(msg),send_to=send_to,subject=subject,template=template,send_from=send_from,content_type=content_type)
    mail.save()

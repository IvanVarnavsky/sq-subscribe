# -*- coding: utf-8 -*-
from string import strip
from django.contrib.sites.models import Site
from django.db import models
from django.template.base import TemplateDoesNotExist
from django.template.loader import find_template_loader

from djcelery.models import PeriodicTask, CrontabSchedule
from sq_core.basemodel.models import BaseModel
from sq_core.baseuser.models import get_user_model
from sq_subscribe.mailqueue.models import CONTENT_TYPE, create_mailqueue
from django.db.models import get_model
from django.conf import settings
from sq_subscribe import subscribe
from sq_subscribe.mailqueue.tasks import send_concrete_mailqueue

class Subscribe(BaseModel):
    SUBSCRIBE_TYPE = [
        ('sometime', u'Одноразовая отправка'),
        ('content', u'Подписка на контент'),
    ]
    WEEKDAYS = [
        ('monday', u'Понедельник'),
        ('tuesday', u'Вторник'),
        ('wednesday', u'Среда'),
        ('thursday', u'Четверг'),
        ('friday', u'Пятница'),
        ('saturday', u'Суббота'),
        ('sunday', u'Воскресенье'),
    ]

    users = models.ManyToManyField(get_user_model(), through='UserSubscribes')
    template = models.TextField(blank=True)
    subscribe_type = models.CharField(u'Формат подписки', max_length=100, choices=SUBSCRIBE_TYPE,default='sometime')
    weekday = models.CharField(u'День недели',null=True,blank=True,choices=WEEKDAYS,default='saturday',max_length=20)
    time = models.CharField(u'Время дня', null=True,blank=True,default='23:00',max_length=5)
    task = models.ForeignKey(PeriodicTask,null=True)
    modelname = models.CharField(u'Подписать на контент',null=True,blank=True,max_length=100) #Должен быть выбор из списка созданных моделей(подгружать в admin.py)
    delete_after_sending = models.BooleanField(u'Удалить после отправки',default=False)
    content_type = models.CharField(u'Формат письма', max_length=100, choices=CONTENT_TYPE,default='plain')
    subject = models.CharField(u'Тема',max_length=1000,null=True,blank=True,default=u'Без темы')
    message = models.TextField(u'Сообщение',blank=True)
    last_send_date = models.DateTimeField(default=None,null=True,blank=True)

    def __unicode__(self):
        return self.subject

    def delete(self, *args, **kwargs):
        if self.task:
            self.task.delete()
        super(Subscribe, self).delete()

    def get_modelname(self):
        if ":" in self.modelname:
            model_app = self.modelname.split(":")
            return get_model(model_app[0],model_app[1])
        return get_model("",self.modelname)

    def create_content_subscribe(self):
        if self.id is None:
            crontab = CrontabSchedule.objects.create()
            task = PeriodicTask.objects.create()
            self.save()
            task.task = "sq_subscribe.subscribe.tasks.build_subsribe_query"
            task.args = [self.id]
        else:
            task = self.task
            crontab = task.crontab
        time = self.time.split(':')
        #TODO добавить валидацию времени
        crontab.hour=strip(time[0])
        crontab.minute=strip(time[1])
        crontab.day_of_week=self.weekday
        crontab.save()
        task.crontab_id = crontab.id
        if self.published:
            task.enabled = True
        else:
            task.enabled = False
        self.save()
        task.name = u'Очередь подписки ({0}) {1}'.format(self.id,subscribe)
        task.save()
        self.task = task
        self.save()
        return self


    def create_sometime_subscribe(self,users):
        content_type = self.content_type if self.content_type == 'html' else 'plain'
        template = load_template(content_type,type='sometime')
        self.template = template
        self.save()
        if users is not None:
            message = {'sitename': Site.objects.get(id=settings.SITE_ID).name,'message':self.message}
            mail_ids = []
            for user in users:
                data_user = {'username':user.username}
                vars = message
                vars.update({'user':data_user})
                mail = create_mailqueue(subject=self.subject,template=self.template,send_to=user.email,
                                 content_type=self.content_type,message=vars)
                mail_ids.append(mail.id)
            send_concrete_mailqueue.delay(mail_ids)
        if self.delete_after_sending:
            self.delete()
        return self


    def add_subscribe_for_user(self,user):
        import hashlib
        key_string = user.username
        salt = str(self.created_date)
        link = hashlib.md5( salt + key_string ).hexdigest()
        user_suscribe = UserSubscribes.objects.get_or_create(user = user ,subscribe = subscribe, unsubscribe_link = link)
        return user_suscribe


    class Meta:
        db_table = 'subscribe'
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'


def load_template(content = 'plain', type = 'content'):
    template_dir =  getattr(settings, "ADMIN_SUBSCRIBE_TEMPLATE_DIR", "email")
    template = None
    if type == 'content':
        if content == 'plain':
            template_name = '{0}.{1}'.format(type,'txt')
        else:
            template_name = '{0}.{1}'.format(type,'html')
        template_path = template_dir + "/" + template_name

        loaders = []
        for loader_name in settings.TEMPLATE_LOADERS:
            loader = find_template_loader(loader_name)
            if loader is not None:
                loaders.append(loader)
        template_source_loaders = tuple(loaders)
        for loader in template_source_loaders:
            try:
                template = loader.load_template_source(template_path)
                return template[0]
            except TemplateDoesNotExist:
                pass
    else:
        if content == 'plain':
            template = '{0}.{1}'.format(type,'txt')
        else:
            template = '{0}.{1}'.format(type,'html')
    return template


class UserSubscribes(models.Model):
    user = models.ForeignKey(get_user_model())
    subscribe = models.ForeignKey(Subscribe)
    unsubscribe_link = models.CharField(max_length=100,blank=True)

    def __unicode__(self):
        return self.user

    class Meta:
        db_table = 'user_subscribes'
        unique_together = (("user", "subscribe"),)


class ContentSubscribe(Subscribe):

    class Meta:
        proxy = True
        verbose_name = 'Подписка на контент'
        verbose_name_plural = 'Подписки на контент'


class SometimeSubscribe(Subscribe):

    class Meta:
        proxy = True
        verbose_name = 'Одноразовая подписка'
        verbose_name_plural = 'Одноразовые подписки'
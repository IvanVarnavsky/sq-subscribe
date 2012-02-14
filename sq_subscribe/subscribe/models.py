# -*- coding: utf-8 -*-
from django.db import models
from djcelery.models import PeriodicTask
from sq_core.basemodel.models import BaseModel
from sq_subscribe.mailqueue.models import CONTENT_TYPE
from django.db.models import get_model
from django.conf import settings

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

    users = models.ManyToManyField(get_model(*settings.CUSTOM_USER_MODEL.split('.')), through='UserSubscribes')
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

    class Meta:
        db_table = 'subscribe'
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

class UserSubscribes(models.Model):
    user = models.ForeignKey(get_model(*settings.CUSTOM_USER_MODEL.split('.')))
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
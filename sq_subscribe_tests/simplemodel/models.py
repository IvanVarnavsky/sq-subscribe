# -*- coding: utf-8 -*-
from django.db import models
from sq_core.basemodel.models import BaseModel

class SimpleModel(BaseModel):
    title = models.CharField(max_length=100)
    text = models.TextField()

    def __unicode__(self):
        return u'Simple Model ' + str(self.title)

    class Meta:
        verbose_name = 'Простая модель'
        verbose_name_plural = 'Простые модели'
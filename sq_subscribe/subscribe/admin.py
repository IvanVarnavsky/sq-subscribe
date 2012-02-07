# -*- coding: utf-8 -*-
from string import strip
from django import forms
from django.conf import settings
from django.contrib import admin
from django.db.models.loading import get_model
from djcelery.admin import LaxChoiceField
from djcelery.models import PeriodicTask, CrontabSchedule
from sq_subscribe.subscribe.models import SometimeSubscribe, ContentSubscribe
from sq_widgets.widgets import HighlighterWidget


def load_models():
    data = {'':'Выберите модель'}
    dictList = []
    if settings.SUBSCRIBED_MODELS is not None:
        for subscribed in settings.SUBSCRIBED_MODELS:
            #TODO нужно обработать вложенность больше одной в apps
            try:
                if "." in subscribed:
                    app_model = subscribed.split('.')
                    model = get_model(app_model[0],app_model[1])
                else:
                    model = get_model("",subscribed)
            except Exception:
                raise Exception('Error loading subscribed model with name: %s'%subscribed)
            data.update({model:model._meta.verbose_name})
        temp = []
        for key, value in data.iteritems():
            temp = [key,value]
            dictList.append(temp)
    return dictList

class ContentSubscribeForm(forms.ModelForm):
    modelname = LaxChoiceField(label=u"Подписать на контент", choices=load_models(),)
    subscribe_type = forms.CharField(label='',widget=forms.HiddenInput,initial='content')
    message = forms.CharField(widget=HighlighterWidget)

    def __init__(self, *args, **kwargs):
         super(ContentSubscribeForm, self).__init__(*args, **kwargs)
         self.fields['weekday'].required = True


    def save(self, commit=True):
        subscribe = super(ContentSubscribeForm, self).save(commit=False)
        if subscribe.id is None:
            crontab = CrontabSchedule.objects.create()
            task = PeriodicTask.objects.create()
            subscribe.save()
            task.task = "sq_subscribe.subscribe.tasks.build_subsribe_query"
            task.args = [subscribe.id]
        else:
            task = subscribe.task
            crontab = task.crontab
        time = subscribe.time.split(':')
        #TODO добавить валидацию времени
        crontab.hour=strip(time[0])
        crontab.minute=strip(time[1])
        crontab.day_of_week=subscribe.weekday
        crontab.save()
        task.crontab_id = crontab.id
        if subscribe.published:
            task.enabled = True
        else:
            task.enabled = False
        subscribe.save()
        task.name = u'Очередь подписки %s'%subscribe
        task.save()
        subscribe.task = task
        subscribe.save()
        return subscribe

    class Meta:
        model = ContentSubscribe

    class Media:
        js = (
            'sq_subscribe/js/jquery-1.6.1.js',
            'sq_subscribe/js/subscribe-0.1.js',
        )
        css = {
            'all': ( 'sq_subscribe/css/style.css',)
        }

class SometimeSubscribeForm(forms.ModelForm):
    subscribe_type = forms.CharField(label='',widget=forms.HiddenInput,initial='sometime',)
    message = forms.CharField(widget=HighlighterWidget)

    def save(self, commit=True):
        subscribe = super(SometimeSubscribeForm, self).save(commit=False)
        subscribe.save()
        return subscribe

    class Meta:
        model = SometimeSubscribe

    class Media:
        js = (
            'sq_subscribe/js/jquery-1.6.1.js',
            'sq_subscribe/js/subscribe-0.1.js',
        )
        css = {
            'all': ( 'sq_subscribe/css/style.css',)
        }


class ContentSubscribeAdmin(admin.ModelAdmin):

    def queryset(self, request):
            return self.model.objects.filter(subscribe_type="content")

    fieldsets = (
        ('Параметры подписки', {
            'classes': ('wide','content_subscribe'),
            'fields': ('modelname','weekday', 'time')
        }),
        (None, {
            'fields': ('content_type','subject','message','published',)
        }),
        (None, {
            'fields': ('subscribe_type',),
            'classes': ('hidden_fieldset',),
        }),
    )
    form = ContentSubscribeForm

class SometimeSubscribeAdmin(admin.ModelAdmin):

    def queryset(self, request):
                return self.model.objects.filter(subscribe_type="sometime")

    fieldsets = (
        ('Параметры подписки', {
            'classes': ('wide','sometime_subscribe'),
            'fields': ('delete_after_sending',)
        }),
        (None, {
            'fields': ('content_type','subject','message','published',)
        }),
        (None, {
            'fields': ('subscribe_type',),
            'classes': ('hidden_fieldset',),
        }),
    )
    form = SometimeSubscribeForm


admin.site.register(ContentSubscribe,ContentSubscribeAdmin)
admin.site.register(SometimeSubscribe,SometimeSubscribeAdmin)

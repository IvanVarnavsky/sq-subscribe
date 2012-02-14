# -*- coding: utf-8 -*-
from string import strip
from django import forms
from django.conf import settings
from django.contrib import admin
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.db.models.loading import get_model
from django.template.base import TemplateDoesNotExist
from django.template.loaders.eggs import  Loader
from djcelery.admin import LaxChoiceField
from djcelery.models import PeriodicTask, CrontabSchedule
from sq_subscribe.subscribe.models import SometimeSubscribe, ContentSubscribe, UserSubscribes
from sq_widgets.widgets import HighlighterWidget, WysiwygWidget


def load_models():
    data = {'':'Выберите модель'}
    dictList = []
    models =  getattr(settings, "SUBSCRIBED_MODELS", False)
    if models:
        for subscribed in settings.SUBSCRIBED_MODELS:
            #TODO нужно обработать вложенность больше одной в apps
            try:
                if "." in subscribed:
                    app_model = subscribed.split('.')
                    model = get_model(app_model[0],app_model[1])
                    model_name = "{0}:{1}".format(app_model[0],app_model[1])
                else:
                    model = get_model("",subscribed)
                    model_name = subscribed
            except Exception:
                raise Exception('Error loading subscribed model with name: %s'%subscribed)
            data.update({model_name:model._meta.verbose_name})
        temp = []
        for key, value in data.iteritems():
            temp = [key,value]
            dictList.append(temp)
    return dictList

 #TODO FIXME
def load_template(content = 'plain', type = 'content'):
    template_dir =  getattr(settings, "ADMIN_SUBSCRIBE_TEMPLATE_DIR", False)
    if not template_dir:
        template_dir = "email"
    if content == 'plain':
        template_path = template_dir+'/{0}.{1}'.format(type,'txt')
    else:
        template_path = template_dir+'/{0}.{1}'.format(type,'html')
    try:
        template = Loader().load_template_source(template_path)[0]
    except TemplateDoesNotExist:
        raise TemplateDoesNotExist('Template path %s does not exist.'%template_path)
    return template

class ContentSubscribeForm(forms.ModelForm):
    modelname = LaxChoiceField(label=u"Подписать на контент", choices=load_models())
    subscribe_type = forms.CharField(label='',widget=forms.HiddenInput,initial='content')
    message = forms.CharField(label=u'Сообщение',widget=HighlighterWidget,initial=load_template())
    hidden_message = forms.CharField(widget=forms.Textarea,required=False,initial=load_template(content='html'))

    def __init__(self, *args, **kwargs):
         super(ContentSubscribeForm, self).__init__(*args, **kwargs)
         self.fields['weekday'].required = True
         instance = getattr(self, 'instance', None)
         hidden_message_template = 'html'
         if instance and instance.id:
            self.fields['modelname'].widget.attrs['disabled'] = True
            self.fields['modelname'].required = False
            if instance.content_type == 'html':
                hidden_message_template = 'plain'
         self.fields['hidden_message'].initial = load_template(hidden_message_template)

    def clean_modelname(self):
        if self.instance and self.instance.id:
            return self.instance.modelname
        else :
            return self.cleaned_data['modelname']


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
        task.name = u'Очередь подписки ({0}) {1}'.format(subscribe.id,subscribe)
        task.save()
        subscribe.task = task
        subscribe.save()
        # ------------ TEST ------------ #
        user = get_model(*settings.CUSTOM_USER_MODEL.split('.')).objects.get(username = 'admin')

        import hashlib
        key_string = user.username
        salt = str(user.date_joined)
        link = hashlib.md5( salt + key_string ).hexdigest()
        userSuscribe = UserSubscribes.objects.get_or_create(user = user ,subscribe = subscribe, unsubscribe_link = link)
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
    message = forms.CharField(label=u'Сообщение',widget=WysiwygWidget)
    select_users = forms.ModelMultipleChoiceField(label=u'Получатели',queryset=get_model(*settings.CUSTOM_USER_MODEL.split('.')).objects.all(), widget=FilteredSelectMultiple(u"Пользователи", is_stacked=False))

    def save(self, commit=True):
        subscribe = super(SometimeSubscribeForm, self).save(commit=False)
        subscribe.save()
        return subscribe

    class Meta:
        model = SometimeSubscribe

    class Media:
        js = (
            'sq_subscribe/js/jquery-1.6.1.js',
#            'sq_subscribe/js/subscribe-0.1.js',
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
            'fields': ('hidden_message','subscribe_type',),
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
            'fields': ('content_type','subject','message','select_users','published',)
        }),
        (None, {
            'fields': ('subscribe_type',),
            'classes': ('hidden_fieldset',),
        }),
    )
    form = SometimeSubscribeForm


admin.site.register(ContentSubscribe,ContentSubscribeAdmin)
admin.site.register(SometimeSubscribe,SometimeSubscribeAdmin)

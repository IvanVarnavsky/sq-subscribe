# -*- coding: utf-8 -*-
from django import forms
from django.conf import settings
from django.contrib import admin
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.db.models.loading import get_model
from djcelery.admin import LaxChoiceField
from sq_user.baseuser.models import get_user_model
from sq_subscribe.subscribe.models import SometimeSubscribe, ContentSubscribe, UserSubscribes, load_template
from sq_widgets.widgets import HighlighterWidget, WysiwygWidget
from sq_subscribe.mailqueue.models import CONTENT_TYPE


def load_models():
    data = {'':'Выберите модель'}
    dictList = []
    models =  getattr(settings, "SUBSCRIBED_MODELS", False)
    if models:
        for subscribed in settings.SUBSCRIBED_MODELS:
            try:
                if "." in subscribed:
                    app_model = subscribed.rsplit('.',1)
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
        return subscribe.create_content_subscribe()

    class Meta:
        model = ContentSubscribe

    class Media:
        js = (
            'js/jquery-1.6.1.js',
            'js/subscribe-0.1.js',
        )
        css = {
            'all': ( 'css/style.css',)
        }

class SometimeSubscribeForm(forms.ModelForm):
    subscribe_type = forms.CharField(label='',widget=forms.HiddenInput,initial='sometime')
    content_type = forms.ChoiceField(label=u'Формат письма',help_text=u'RICH текст при изменении формата письма не сохранятеся!',choices=CONTENT_TYPE,)
    message = forms.CharField(label=u'Сообщение',widget=WysiwygWidget(load_on_startup=False))
    select_users = forms.ModelMultipleChoiceField(label=u'Получатели',queryset=get_user_model().objects.all(), widget=FilteredSelectMultiple(u"Пользователи", is_stacked=False),required=False)

    def save(self, commit=True):
        subscribe = super(SometimeSubscribeForm, self).save(commit=False)
        return subscribe.create_sometime_subscribe(self.cleaned_data['select_users'])


    class Meta:
        model = SometimeSubscribe

    class Media:
        js = (
            'js/jquery-1.6.1.js',
            'js/subscribe-0.1.js',
        )
        css = {
            'all': ( 'css/style.css',)
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

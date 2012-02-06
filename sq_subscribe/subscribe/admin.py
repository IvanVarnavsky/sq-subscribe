# -*- coding: utf-8 -*-
from string import strip
from django import forms
from django.contrib import admin
from django.contrib.admin.widgets import AdminIntegerFieldWidget
from djcelery.models import PeriodicTask, CrontabSchedule
from sq_subscribe.subscribe.models import Subscribe

#class SubscribeAdminWidget(AdminIntegerFieldWidget):
#
#    def render(self, name, value, attrs=None):
#        attrs = {'type':'hidden','class':'image_upload_field'}
#        uploaderCode = '<input type="file" id="fileupload"> <div class="image_upload_preview"></div>'
#        data =  super(ImageUploaderAdminWidget,self).render(name,value,attrs)
#        data += uploaderCode
#        return data
#
#    class Media:
#            js = (
#                'js/jquery/jquery-1.6.1.js',
#                'sq_admin/js/jquery.ui.widget.js',
#                'sq_admin/js/jquery.iframe-transport.js',
#                'sq_admin/js/jquery.fileupload.js',
#                'sq_admin/js/jquery.xdr-transport.js',
#                'sq_admin/js/imageuploader.js',
#            )

class SubscribeForm(forms.ModelForm):

    def save(self, commit=True):
        subscribe = super(SubscribeForm, self).save(commit=False)
        if subscribe.id is None:
            if subscribe.subscribe_type == 'content':
                time = subscribe.time.split(':')
                crontab = CrontabSchedule.objects.create(hour=strip(time[0]), minute=strip(time[1]), day_of_week=subscribe.weekday)
                crontab.save()
                task = PeriodicTask.objects.create(name = u'Очередь подписки %s'%subscribe)
                task.crontab_id = crontab.id
                if subscribe.published:
                    task.enabled = True
                subscribe.task = task
                subscribe.save()
                task.task = "sq_subscribe.subscribe.tasks.build_subsribe_query"
                task.args = [subscribe.id]
                task.save()
            else:
                pass
        else:
            if subscribe.subscribe_type == 'content':
                task = subscribe.task
                time = subscribe.time.split(':')
                crontab = task.crontab
                crontab.hour=strip(time[0])
                crontab.minute=strip(time[1])
                crontab.day_of_week=subscribe.weekday
                crontab.save()
                if subscribe.published:
                    task.enabled = True
                subscribe.save()
                task.name = u'Очередь подписки %s'%subscribe
                task.save()
            else:
                pass
        subscribe.save()
        return subscribe

    class Meta:
        model = Subscribe

    class Media:
        js = (
            'sq_subscribe/js/jquery-1.6.1.js',
            'sq_subscribe/js/subscribe-0.1.js',
        )


class SubscribeAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('subscribe_type', )
        }),
        ('Параметры подписки', {
            'classes': ('wide','content_subscribe'),
            'fields': ('modelname','weekday', 'time')
        }),
        ('Параметры подписки', {
            'classes': ('wide','sometime_subscribe'),
            'fields': ('delete_after_sending',)
        }),
        (None, {
            'fields': ('content_type','subject','message','published')
        }),
    )
    exclude = ('template','task',)
    form = SubscribeForm


admin.site.register(Subscribe,SubscribeAdmin)

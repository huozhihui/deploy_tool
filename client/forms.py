#!/usr/bin/python
# -*- coding: utf-8 -*-
from django import forms
from models import *
from django.forms import ModelForm, Textarea
from django.utils.translation import ugettext_lazy as _, ungettext_lazy

# class HostForm(forms.Form):
#     username = forms.CharField(label='用户名', max_length=30)
#     password = forms.CharField(label='密码', max_length=30)
#     ip = forms.GenericIPAddressField(label='IP')
#     port = forms.IntegerField(label='端口')
#     describe = forms.CharField(label='描述', max_length=255)
default_errors = {
    'required': _('This field is required'),
    'invalid': _('Enter a valid value')
}

class DynamicVarForm(ModelForm):
    class Meta:
        model = DynamicVar
        fields = ['name', 'describe']

class RoleManageForm(ModelForm):
    class Meta:
        model = RoleManage
        fields = ['name', 'timeout']
    # name = forms.CharField(label=u'名称', max_length=30, error_messages=default_errors)
    # timeout = forms.IntegerField(label=u'运行时长', error_messages=default_errors)


class HostGroupForm(ModelForm):
    class Meta:
        model = HostGroup
        fields = ['name', 'describe']
        widgets = {'describe': Textarea(attrs={'cols': 40, 'rows': 10})}


class HostForm(ModelForm):
    # host_roles = forms.CharField(widget=forms.HiddenInput(attrs={'class': 'hidden'}))

    class Meta:
        model = Host
        fields = ['username', 'password', 'ip', 'port', 'describe']
        widgets = {
            'describe': Textarea(attrs={'cols': 40, 'rows': 10})
        }
        error_messages = {
            'ip': {
                'invalid': _("Enter a valid IPv4 or IPv6 address"),
            },
        }
        # exclude = ['title']
        # for visible in form.visible_fields():
        #     visible.field.widget.attrs['class'] = 'form-control'

        # labels = {
        #     'name': _('Writer'),
        # }
        # help_texts = {
        #     'name': _('Some useful help text.'),
        # }
        # error_messages = {
        #     'name': {
        #         'max_length': _("This writer's name is too long."),
        #     },
        # }


class BaseForm(forms.Form):
    TO_HIDE_ATTRS = {'class': 'hidden'}
    c_remove = [('no', u'创建'), ('yes', u'删除')]
    yes_or_no = [('yes', u'是'), ('no', u'否')]
    STATE = [('present', u'创建'), ('absent', u'删除')]
    hosts = forms.CharField(widget=forms.HiddenInput)
    FILESTATE = [('directory', u'创建目录'),
                 ('touch', u'创建文件'),
                 ('link', u'创建软链接'),
                 ('hard', u'创建硬链接'),
                 ('absent', u'删除文件、目录或取消链接')]


class CreateUserForm(BaseForm):
    remove = forms.ChoiceField(label=u'操作方式', choices=BaseForm.c_remove, widget=forms.RadioSelect())
    name = forms.CharField(label=u'用户名', max_length=30, error_messages=default_errors)
    password = forms.CharField(label=u'密码', max_length=30, required=False)
    home = forms.CharField(label=u'Home', max_length=30, required=False)
    shell = forms.CharField(label=u'Shell', max_length=30, required=False)
    system = forms.ChoiceField(label=u'是否管理员', choices=BaseForm.yes_or_no, widget=forms.RadioSelect())


class CreateGroupForm(BaseForm):
    state = forms.ChoiceField(label=u'操作方式', choices=BaseForm.STATE, widget=forms.RadioSelect())
    name = forms.CharField(label=u'组名', max_length=30, error_messages=default_errors)
    system = forms.ChoiceField(label=u'是否系统组', choices=BaseForm.yes_or_no, widget=forms.RadioSelect())


class CreateFileForm(BaseForm):
    state = forms.ChoiceField(label=u'操作方式', choices=BaseForm.FILESTATE, widget=forms.Select())
    src = forms.CharField(label=u'源路径', max_length=80, error_messages=default_errors)
    dest = forms.CharField(label=u'目标路径', max_length=80, error_messages=default_errors)


class SendCmdForm(BaseForm):
    cmd = forms.CharField(label=u'命令', max_length=30)


class SendFileForm(BaseForm):
    src = forms.FileField(label=u'本地文件')
    dest = forms.CharField(label=u'远程目录', max_length=80)
    backup = forms.ChoiceField(label=u'是否备份', choices=BaseForm.yes_or_no, widget=forms.RadioSelect())
    owner = forms.CharField(label=u'所有者', max_length=50, required=False)
    group = forms.CharField(label=u'组', max_length=50, required=False)
    mode = forms.CharField(label=u'权限', max_length=10, required=False)

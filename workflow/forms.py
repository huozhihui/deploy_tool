#!/usr/bin/python
# -*- coding: utf-8 -*-
from django import forms
from models import *
from client.models import RoleManage
from django.forms import ModelForm, Textarea
from django.utils.translation import ugettext_lazy as _, ungettext_lazy

class HomeWorkForm(ModelForm):
    class Meta:
        model = HomeWork
        fields = ['name', 'describe']
        widgets = {'describe': Textarea(attrs={'cols': 40, 'rows': 10})}

class ParameterForm(ModelForm):
    name = forms.CharField(label=u'参数名称', max_length=30)
    # role_names = forms.ChoiceField(label=u'角色')

    class Meta:
        model = Parameter
        fields = ['name', 'value']
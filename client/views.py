#!/usr/bin/python
# -*- coding: utf-8 -*-
from forms import HostForm
from models import Host, RoleManage
from collections import defaultdict
from client.controllers import *

# class HostListView(ListView):
#     class_name = 'host'
#     title_name = '客户端'
#     template_name = '{0}/{1}'.format(class_name, 'index.html')
#
#     def get_queryset(self):
#         return ext_helper.get_objects(self.request, self.class_name.title())
#
#     def get_context_data(self, **kwargs):
#         context = super(HostListView, self).get_context_data(**kwargs)
#         context['title_name'] = self.title_name
#         return context
#
# class HostCreate(CreateView):
#     model = Host
#     title_name = '客户端'
#     operation = "添加"
#     fields = ['username']
#     template_name = "host/form.html"
#     def get_context_data(self, **kwargs):
#         context = super(HostCreate, self).get_context_data(**kwargs)
#         context['title_name'] = self.title_name
#         return context

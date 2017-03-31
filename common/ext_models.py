#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


# 基类
class Base(models.Model):
    user = models.ForeignKey(User)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def class_name(self):
        return self.__class__.__name__.lower()
    class Meta:
        abstract = True

# 基类
class CommonName(models.Model):
    name = models.CharField("名称", max_length=30)
    def __unicode__(self):
        return self.name
    class Meta:
        abstract = True

# 基类
class CommonDescribe(models.Model):
    describe = models.CharField("描述", max_length=255, blank=True, null=True)
    def __unicode__(self):
        return self.describe
    class Meta:
        abstract = True

# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-10 18:31
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0019_dynamic_variable_host_role_dynamic_variable'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rolemanage',
            name='dynamic_vars',
        ),
    ]

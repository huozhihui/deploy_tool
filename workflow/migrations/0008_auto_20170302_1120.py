# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-03-02 03:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workflow', '0007_tasklog_role_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='parameter',
            name='pgroup',
        ),
        migrations.AddField(
            model_name='parameter',
            name='role_name',
            field=models.CharField(default=2, max_length=30, verbose_name='\u89d2\u8272'),
            preserve_default=False,
        ),
    ]

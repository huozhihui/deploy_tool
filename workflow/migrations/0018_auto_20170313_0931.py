# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-13 09:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workflow', '0017_auto_20170312_2314'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task_result',
            name='task_name',
            field=models.CharField(max_length=255, verbose_name='\u4efb\u52a1\u540d\u79f0'),
        ),
    ]

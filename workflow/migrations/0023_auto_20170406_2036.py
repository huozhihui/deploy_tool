# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-06 20:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workflow', '0022_tasklog_step_count'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tasklog',
            name='content',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
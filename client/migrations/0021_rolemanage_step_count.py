# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-13 01:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0020_remove_rolemanage_dynamic_vars'),
    ]

    operations = [
        migrations.AddField(
            model_name='rolemanage',
            name='step_count',
            field=models.IntegerField(default=0),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-12 23:10
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('workflow', '0015_auto_20170312_2308'),
    ]

    operations = [
        migrations.CreateModel(
            name='Task_Result',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_name', models.CharField(max_length=20, verbose_name='\u4efb\u52a1\u540d\u79f0')),
                ('content', models.CharField(max_length=255, verbose_name='\u8be6\u7ec6\u5185\u5bb9')),
                ('ansible_status', models.CharField(max_length=10, verbose_name='\u4efb\u52a1\u72b6\u6001')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('task_log', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workflow.TaskLog')),
            ],
        ),
    ]
#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from common.ext_models import Base, CommonName, CommonDescribe
from django.utils.translation import ugettext_lazy as _
import time
from client.models import Host, RoleManage, Role_Dynamic_Variable


class HomeWork(CommonDescribe, CommonName, Base):
    pass


class Parameter(CommonName, Base):
    homework = models.ForeignKey(HomeWork)
    role_manage = models.ForeignKey(RoleManage)
    value = models.CharField("值", max_length=60)
    is_dynamic_var = models.BooleanField(default=False)
    # role_name = models.CharField("角色", max_length=30, blank=True, null=True)


class Task(Base):
    homework = models.ForeignKey(HomeWork)
    role_names = models.CharField(max_length=255)
    params = models.TextField(blank=True, null=True)
    uuid = models.CharField(max_length=20)
    status = models.IntegerField()

    # 判断该任务是否结束
    def is_completed(self):
        status_list = list(self.tasklog_set.all().values_list('status', flat=True))
        if (0 in status_list) or (1 in status_list):
            return False
        else:
            return True


    def status_name(self):
        STATUS = {"0": "待部署", "1": "正在部署", "2": "部署完成"}
        return STATUS[str(self.status)]

    def role_manages(self):
        task_logs = self.tasklog_set.all()
        return set([task_log.role_manage for task_log in task_logs])


# child_task
class TaskLog(Base):
    task = models.ForeignKey(Task)
    host = models.ForeignKey(Host)
    role_manage = models.ForeignKey(RoleManage)
    num = models.IntegerField(verbose_name="序号")
    content = models.CharField(max_length=255, blank=True, null=True)
    status = models.IntegerField()
    begin_deploy_at = models.DateTimeField(blank=True, null=True)
    ansible_status = models.CharField(max_length=10, blank=True, null=True)
    # role_name = models.CharField(max_length=30, blank=True, null=True)
    step_count = models.IntegerField(default=0)
    timeout = models.IntegerField(default=180)

    # def __str__(self):
    #     return self.id

    # Redis-key
    def redis_key(self):
        return "{id}-{ip}".format(id=self.id, ip=self.host.ip)

    # 任务在redis中详细信息
    def redis_key_info(self):
        return "{redis_key}-info".format(redis_key=self.redis_key())

    # 任务在redis中结果
    def redis_key_result(self):
        return "{redis_key}-result".format(redis_key=self.redis_key())

    # 总步骤数

    #当前步骤
    def current_step(self):
        return len(self.task_result_set.all())

    def progress_per(self):
        try:
            per = self.current_step() * 100 / float(self.step_count)
        except:
            per = 0
        return "{0:.0f}%".format(per)


    # 剩余时间
    # def rest_time(self):
    #     return time.strftime('%H:%M:%S', time.gmtime(self.timeout))

    # 耗时
    # def use_time(self):
    #     num = self.role_manage.timeout - self.timeout
    #     return "{num}s".format(num=num)

    def status_name(self):
        STATUS = {"0": "待部署", "1": "正在部署", "2": "部署成功", "3": "部署失败", "4": "连接失败"}
        return STATUS[str(self.status)]

    def color(self):
        if self.status == 3 or self.status == 4:
            c = 'red'
        elif self.status == 2:
            c = 'green'
        else:
            c = ''
        return c


class Task_Result(models.Model):
    task_log = models.ForeignKey(TaskLog)
    task_name = models.CharField("任务名称", max_length=255)
    content = models.TextField("返回结果", blank=True, null=True)
    ansible_status = models.CharField("任务状态", max_length=10, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def class_name(self):
        return self.__class__.__name__.lower()

    def __str__(self):
        return self.task_name

    def __unicode__(self):
        return unicode(self.task_name) or u''

    def task_is_failed(self):
        if self.ansible_status not in ['ok', 'changed', 'skipped']:
            return True
        else:
            return False

    def color(self):
        c = 'green'
        if self.task_is_failed():
            c = 'red'
        return c

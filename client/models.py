#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from common.ext_models import Base, CommonName, CommonDescribe
from django.utils.translation import ugettext_lazy as _



class DynamicVar(CommonDescribe, CommonName, Base):
    name = models.CharField("名称", max_length=20, unique= True)
    def __str__(self):
        return self.name

    def __unicode__(self):
        return unicode(self.name) or u''

class RoleManage(CommonDescribe, CommonName, Base):
    # name = models.CharField("名称", max_length=20, unique= True)
    # name===》Ansible hosts分组用到
    # playbook===》Ansible-playbook脚本用到
    # tag===》标示Ansible-playbook 参数分组

    # name = models.CharField("名称", max_length=20)
    num = models.IntegerField(verbose_name="顺序编号")
    timeout = models.IntegerField(verbose_name="超时时长(s)", default=180)
    playbook = models.CharField("Playbook", max_length=255, blank=True, null= True)
    playbook_name = models.CharField("Playbook名称", max_length=50, blank=True, null= True)
    # playbook子任务数
    # step_count = models.IntegerField(default=0)
    # dynamic_vars = models.CharField("动态变量", max_length=255, blank=True, null= True)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return unicode(self.name) or u''

    def host_ips(self):
        host_roles = self.host_role_set.all()
        return [host_role.host.ip for host_role in host_roles]

    def host_count(self):
        return len(self.host_ips())

    # def playbook_name(self):
    #     return self.playbook.split('.')[0]

    # 角色关联的动态参数
    def dynamic_variable_ids(self):
        role_dynamic_variables = self.role_dynamic_variable_set.all()
        return [rdv.dynamic_var.id for rdv in role_dynamic_variables]

class HostGroup(CommonName, Base):
    describe = models.CharField("描述", max_length=255, blank=True, null= True)

class Host(Base):
    # ip_addr = IPAddressField()
    # host_roles = models.CharField("角色", max_length=100, default='default_role')
    # host_group = models.ForeignKey(HostGroup, verbose_name="隶属组")
    username = models.CharField("用户名", max_length=30)
    password = models.CharField(_('password'), max_length=30)
    # ssh_key = models.CharField("SSH key", max_length=255, blank=True, null= True)
    ip = models.GenericIPAddressField("IP")
    port = models.IntegerField("端口", default=22)
    conn_status = models.BooleanField("连接状态", default=False)
    describe = models.CharField("备注", max_length=255, blank=True, null= True)

    def __str__(self):
        return self.ip

    def status(self):
        STATUS = {0: "离线", 1: "在线"}
        return STATUS[int(self.conn_status)]

    def role_names(self):
        host_roles = self.host_role_set.all()
        role_name_list = [host_role.role_manage.name for host_role in host_roles]
        return ','.join(role_name_list)


class Host_Role(Base):
    host = models.ForeignKey(Host)
    role_manage = models.ForeignKey(RoleManage)

class Dynamic_Variable_Host(Base):
    dynamic_var = models.ForeignKey(DynamicVar)
    host = models.ForeignKey(Host)

class Role_Dynamic_Variable(Base):
    role_manage = models.ForeignKey(RoleManage)
    dynamic_var = models.ForeignKey(DynamicVar)







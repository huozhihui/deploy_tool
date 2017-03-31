#!/usr/bin/python
# -*- coding: utf-8 -*-


import yaml
with open('/Users/huozhihui/huo/paas_deploy/roles/ntp/tasks/main.yml', 'r+') as f:
# with open('/Users/huozhihui/huo/paas_deploy/ntp.yml', 'r+') as f:
# with open('/Users/huozhihui/huo/ansible/user.yaml', 'r+') as f:
    date = yaml.load(f)
    # roles = date[0].get('tasks', None)
    print date
    # print roles
    print len(date)
    # for role in roles:
    #     path = "/Users/huozhihui/huo/paas_deploy/roles/{playbook}/tasks/main.yml".format(playbook=role)
    #     with open(path, 'r+') as s:
    #         main = yaml.load(s)
    #         print len(main)

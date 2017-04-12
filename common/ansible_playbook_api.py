#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
from ansible.parsing.dataloader import DataLoader
from ansible.vars import VariableManager
from ansible.inventory import Inventory
from ansible.executor.playbook_executor import PlaybookExecutor
from ansible.plugins.callback import CallbackBase
from common.redis_api import Rs

# from common.ansible_api import ResultCallback



class ResultCallback(CallbackBase):
    def __init__(self, tid):
        super(ResultCallback, self).__init__()
        self.tid = tid

    def v2_runner_on_ok(self, result, **kwargs):
        print "ok"
        self.v2_runner('ok', result)

    def v2_runner_on_failed(self, result, **kwargs):
        print "failed"
        self.v2_runner('failed', result)

    def v2_runner_on_unreachable(self, result, **kwargs):
        print "unreachable"
        self.v2_runner('unreachable', result)

    def v2_runner_on_skipped(self, result, **kwargs):
        print "skipped"
        self.v2_runner('skipped', result)

    # print dir(result)
    # print result.is_changed()
    # print result.is_failed()
    # print result.is_unreachable()
    # print result.is_skipped()
    def v2_runner(self, status, result):
        task_name = unicode(result._task.name)
        if task_name:
            if result.is_unreachable() or result.is_failed():
                content = result._result.get('stderr', '') or result._result.get('msg', '')
            else:
                if result.is_changed():
                    status = 'changed'
                content = json.dumps(result._result)
        else:
            if result.is_unreachable():
                task_name = u"连接失败"
            if result.is_failed():
                task_name = u"部署失败"
            content = result._result.get('stderr', '') or result._result.get('msg', '')
        print "*******************************************************************"
        print u"执行主机: {ip}".format(ip=result._host.name)
        print u"任务名称: {task_name}".format(task_name=task_name)
        print u"任务结果: {content}".format(content=content)
        if content:
            data = {'task_log_id': self.tid, 'task_name': task_name, 'content': content, 'ansible_status': status}
            ip = result._host.name
            key = "{tid}-{ip}-result".format(tid=self.tid, ip=ip)
            Rs.rpush(key, json.dumps(data))

class Options(object):
    '''
    这是一个公共的类,因为ad-hoc和playbook都需要一个options参数
    并且所需要拥有不同的属性,但是大部分属性都可以返回None或False
    因此用这样的一个类来省去初始化大一堆的空值的属性
    '''

    def __init__(self):
        self.connection = "ssh"
        self.forks = 15
        self.become_user = 'root'
        self.become_method = 'sudo'
        # self.ask_pass = "root"
        # self.ask_become_pass = "huo244"
        self.verbose = "-vvv"
        self.check = False

    def __getattr__(self, name):
        return None


def api(tid, host_list, yml_list, extra_vars={}):
    print 'task id: {tid}'.format(tid=tid)
    print 'yml path: {yml}'.format(yml=yml_list)
    print 'extra_vars: {extra_vars}'.format(extra_vars=extra_vars)
    loader = DataLoader()  # 用来加载解析yaml文件或JSON内容,并且支持vault的解密
    variable_manager = VariableManager()  # 管理变量的类,包括主机,组,扩展等变量,之前版本是在 inventory 中的
    inventory = Inventory(loader=loader, variable_manager=variable_manager, host_list=host_list)
    variable_manager.set_inventory(inventory)  # 根据 inventory 加载对应变量

    options = Options()
    results_callback = ResultCallback(tid)
    playbooks = yml_list  # 这里是一个列表, 因此可以运行多个playbook
    # variable_manager.extra_vars={"ansible_ssh_user":"root" , "ansible_ssh_pass":"root"}  # 增加外部变量

    variable_manager.extra_vars = extra_vars  # 增加外部变量
    pb = PlaybookExecutor(playbooks=playbooks, inventory=inventory, variable_manager=variable_manager, loader=loader,
                          options=options, passwords=None)
    pb._tqm._stdout_callback = results_callback
    result = pb.run()
    return result


if __name__ == '__main__':
    # yml_list = ['/Users/huozhihui/huo/ansible/user.yaml']
    tid = '1'
    host_list = '/Users/huozhihui/huo/paas_deploy/hosts'
    yml_list = ['/etc/ansible/roles/nginx_install.yaml']
    yml_list = ['/Users/huozhihui/huo/ansible/roles/mysql_install/tasks/main.yaml']
    yml_list = ['/Users/huozhihui/huo/paas_deploy/ntp.yml']
    extra_vars = {
        # "ansible_ssh_user": "huo",
        # "ansible_ssh_pass": "huo244",
        # "ip": '20.20.20.0'
    }
    api(tid, host_list, yml_list, extra_vars)
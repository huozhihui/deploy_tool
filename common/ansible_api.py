#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import datetime
import random
from common.redis_api import Rs
from ansible.parsing.dataloader import DataLoader
from ansible.vars import VariableManager
from ansible.inventory import Inventory
from ansible.playbook.play import Play
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.executor.playbook_executor import PlaybookExecutor
from ansible.plugins.callback import CallbackBase
loader = DataLoader()                     # 用来加载解析yaml文件或JSON内容,并且支持vault的解密
variable_manager = VariableManager()      # 管理变量的类,包括主机,组,扩展等变量,之前版本是在 inventory 中的
inventory = Inventory(loader=loader, variable_manager=variable_manager)
variable_manager.set_inventory(inventory) # 根据 inventory 加载对应变量

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

    def v2_runner(self, status, result):
        stdout = ''
        stderr = ''
        color_style = 'green'
        ip = result._host.name
        key = "{tid}-{ip}".format(tid=self.tid, ip=ip)
        if status == "ok":
            if result._result['changed']:
                status = 'changed'
            stdout = self._get_result(result._result, status)
        else:
            print result._result
            stderr = result._result.get('stderr', '') or result._result.get('msg', '')
            color_style = 'red'

        date = {'ip': ip, 'status': status, 'stdout': stdout, 'stderr': stderr, 'color_style': color_style}
        Rs.hmset(key, date)

    def _get_result(self, result, status):
        module_name = result['invocation'].get('module_name', '')
        module_args = result['invocation']['module_args']
        # 用户或组
        if (module_name == 'user' or module_name == "group"):
            msg = self._user_group_msg(module_name, module_args, status)
        # 文件
        elif module_name == 'file':
            msg = self._file_msg(module_name, module_args, status)
        # 下发文件
        elif module_name == '':
            src = module_args.get('src', None)
            if src:
                filename = module_args.get('original_basename', '')
                msg = "Send file {filename} successfully.".format(filename = filename)
        else:
            msg = "Execute Successfully."
        return result.get('stdout', msg)

    def _user_group_msg(self, module_name, module_args, status):
        name = module_args['name']
        state = module_args['state']
        m = dict()
        m['present_ok'] = "Warn: {m_name} {name} already exists.".format(name=name, m_name=module_name)
        m['present_changed'] = "Create {m_name} {name} successfully.".format(name=name, m_name=module_name)
        m['absent_ok'] = "Warn: {m_name} {name} not exists.".format(name=name, m_name=module_name)
        m['absent_changed'] = "Remove {m_name} {name} successfully.".format(name=name, m_name=module_name)
        s = "{state}_{status}".format(state=state, status=status)
        return m[s]

    def _file_msg(self, module_name, module_args, status):
        name = module_args['path']
        state = module_args['state']
        if state == 'hard':
            state = 'hard link'
        if state == 'absent':
            if status == 'ok':
                msg = "Warn: {name} not exists.".format(name=name)
            else:
                msg = "Remove {name} successfully.".format(name=name)
        else:
            if status == 'ok':
                msg = "Warn: {m_name} {name} already exists.".format(m_name=state, name=name)
            else:
                msg = "Create {m_name} {name} successfully.".format(m_name=state, name=name)

        return msg

class Options(object):
    '''
    这是一个公共的类,因为ad-hoc和playbook都需要一个options参数
    并且所需要拥有不同的属性,但是大部分属性都可以返回None或False
    因此用这样的一个类来省去初始化大一堆的空值的属性
    '''
    def __init__(self):
        self.connection = "local"
        self.forks = 1
        self.check = False
    def __getattr__(self, name):
        return None


def api(tid, module_name, hosts, params, extra_vars={}):
    options = Options()
    results_callback = ResultCallback(tid)
    variable_manager.extra_vars= extra_vars  # 增加外部变量
    # 构建pb, 这里很有意思, 新版本运行ad-hoc或playbook都需要构建这样的pb, 只是最后调用play的类不一样
    # :param name: 任务名,类似playbook中tasks中的name
    # :param hosts: playbook中的hosts
    # :param tasks: playbook中的tasks, 其实这就是playbook的语法, 因为tasks的值是个列表,因此可以写入多个task
    play_source = {"name": "Ansible Ad-Hoc",
                   "hosts": hosts,
                   "gather_facts": "no",
                   "tasks":[
                       # {"action":{"module":"shell","args":"w"}}
                       {"action":{"module":module_name,"args": params}}
                   ]
                   }
    play = Play().load(play_source, variable_manager=variable_manager, loader=loader)
    tqm = None
    try:
        tqm = TaskQueueManager(
            inventory=inventory,
            variable_manager=variable_manager,
            loader=loader,
            options=options,
            passwords=None,
            stdout_callback=results_callback,
            run_tree=False,
        )

        result = tqm.run(play)
        print result
    finally:
        if tqm is not None:
            tqm.cleanup()



if __name__ == '__main__':
    ext_vars = {"ansible_ssh_user":"root" , "ansible_ssh_pass":"root"}
    # params = {"name": "user01", "state": "absent", "remove": "yes"}
    params = {"name": "user05", "password": "abc"}
    dt = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    rand = random.randint(10, 99)
    tid = "{dt}-{rand}".format(dt=dt, rand=rand)
    api(tid, 'user', '10.200.6.44, 10.200.7.233', params, ext_vars)

    # api(tid, 'user', '10.200.6.44', params, ext_vars)


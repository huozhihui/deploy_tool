#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.db import transaction
from workflow.controllers import *
from workflow.models import Task, TaskLog, HomeWork, RoleManage


def ws_get_deploy_result(tid, task_log_id):
    task_log_id = ext_helper.to_int(task_log_id)
    task = Task.objects.get(id=tid)
    task_log = TaskLog.objects.get(id=task_log_id)
    data = {
        'id': task_log.id,
        'status': task_log.status,
        'status_name': task_log.status_name(),
        'use_time': task_log.use_time()
    }

    # 待部署的状态
    if task_log.status == 0:
        _set_deploy(task, task_log, data)

    if task_log.status == 1:
        _get_deploy_result(task, task_log, data)
    return json.dumps(data)


# 重新部署
@transaction.atomic
def retry_deploy(request, id):
    id = ext_helper.to_int(id)
    tid = request.session.get('tid')
    task_logs = TaskLog.objects.filter(pk=id)
    try:
        # 事务处理
        task_logs.update(
            content="",
            status=0,
            ansible_status="",
            begin_deploy_at=datetime.now(),
            timeout=task_logs[0].role_manage.timeout
        )
        Task.objects.filter(id=tid).update(status=1)
        msg = "success"
    except Exception, e:
        msg = e.message
    task_log = TaskLog.objects.get(pk=id)
    return HttpResponse(json.dumps({'msg': msg, 'status_name': task_log.status_name()}),
                        content_type='application/json')


# 待部署的状态
def _set_deploy(task, task_log, data):
    tid = task.id
    host_ip = task_log.host.ip
    params = json.loads(task.params)
    playbook_name = task_log.role_manage.playbook_name()
    content = '开始安装部署{playbook_name}......'.format(playbook_name=playbook_name)
    print '主机{host_ip}{content}'.format(host_ip=host_ip, content=content)
    try:
        _playbook_api(tid, params, task_log.role_manage.playbook)
        data.update({'status': 1, 'status_name': u"正在部署"})
        content = '调用{playbook_name} playbook成功!'.format(playbook_name=playbook_name)
        print '主机{host_ip}{content}'.format(host_ip=host_ip, content=content)
    except Exception, e:
        data.update({'status': 3, 'status_name': u"部署失败"})
        content = '调用{playbook_name} playbook失败, {error_msg}'.format(playbook_name=playbook_name, error_msg=e)
        print '主机{host_ip}{content}'.format(host_ip=host_ip, content=content)
    TaskLog.objects.filter(id=task_log.id).update(status=data['status'], content=content,
                                                  begin_deploy_at=datetime.now())


@ext_helper.thread_method
def _get_deploy_result(task, task_log, data):
    playbook_name = task_log.role_manage.playbook_name()
    content = "正在获取{playbook_name} playbook运行结果......".format(playbook_name=playbook_name)
    if task_log.timeout == 0:
        if task_log.timeout == 0:
            data.update({'status': 3, 'status_name': u"部署失败"})
            content = '{playbook_name} playbook运行超时!'.format(playbook_name=playbook_name)
            print '主机{host_ip}部署{content}'.format(host_ip=task_log.host.ip, content=content)
    # else:
    #     data.update({'status': 3, 'status_name': u"部署失败"})
    #     content = '运行{playbook_name} playbook时开始时间为空,不能判断运行是否超时!'.format(playbook_name=playbook_name)
    #     print '主机{host_ip}{content}'.format(host_ip=task_log.host.ip, content=content)

    key = '{tid}-{ip}'.format(tid=task.id, ip=task_log.host.ip)
    rs_date = redis_api.Rs.hgetall(key)
    ansible_status = rs_date.get('status', None)
    if ansible_status:
        if ansible_status in ['ok', 'changed']:
            data.update({'status': 2, 'status_name': u"部署成功"})
            # date_status = 2
            # date_status_name = '部署成功'
            content = rs_date.get('stdout', None)
        else:
            data.update({'status': 3, 'status_name': u"部署失败"})
            # date_status = 3
            # date_status_name = '部署失败'
            content = rs_date.get('stderr', None)

        # 清除redis缓存
        redis_api.Rs.delete(key)
    TaskLog.objects.filter(id=task_log.id).update(status=data['status'],
                                                  ansible_status=ansible_status,
                                                  content=content)


# 调用playbook_api 接口
@ext_helper.thread_method
def _playbook_api(tid, params, playbook):
    # 将params插入到额外变量
    extra_vars = params
    yaml_path = os.path.join(settings.ANSIBLE_YAMLS, playbook)
    yaml_list = [str(yaml_path)]
    code = ansible_playbook_api.api(tid, yaml_list, extra_vars)


# 实时更新剩余时间
def update_rest_time(request, id):
    id = ext_helper.to_int(id)
    task_logs = TaskLog.objects.filter(pk=id)
    timeout = task_logs[0].timeout
    if timeout != 0:
        timeout = timeout - 1
        task_logs.update(timeout=timeout)
    msg = time.strftime('%H:%M:%S', time.gmtime(timeout))
    return HttpResponse(json.dumps({'msg': msg}), content_type='application/json')

#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.db import transaction
from workflow.controllers import *
from workflow.models import Task, TaskLog, HomeWork, RoleManage, Task_Result


def index(request):
    title_name = _title_name()
    class_name = _class_name()
    msg = ext_helper.get_msg(request)
    object_list = ext_helper.get_objects(request, 'TaskLog')
    render_url = "%s/%s" % (_class_name(), 'index.html')
    return render_to_response(render_url, locals())


def select(request, id):
    id = ext_helper.to_int(id)
    class_name = _class_name()
    task = Task.objects.get(pk=id)
    homework = task.homework
    title_name = homework.name
    msg = ext_helper.get_msg(request)
    object_list = task.tasklog_set.all()
    render_url = "%s/%s" % (_class_name(), 'select.html')
    return render_to_response(render_url, locals())


def delete(request, id):
    id = ext_helper.to_int(id)
    obj = TaskLog.objects.get(pk=id)
    obj.delete()
    if obj.id:
        request.session['msg'] = "数据删除失败!"
    else:
        request.session['msg'] = "数据删除成功!"
    return index(request)


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


# 待部署的状态
def _set_deploy(task, task_log, data):
    tid = task.id
    host_ip = task_log.host.ip
    params = json.loads(task.params)
    # 如果事pre_install 角色,切换ubuntu用户
    if task_log.role_manage.name == 'pre_install':
        params['ansible_ssh_user'] = settings.ANSIBLE_INIT_USER
        params['ansible_ssh_pass'] = settings.ANSIBLE_INIT_PASS

    playbook_name = task_log.role_manage.playbook_name
    msg = '开始安装部署{playbook_name}......'.format(playbook_name=playbook_name)
    content = [msg]
    print '主机{host_ip}{content}'.format(host_ip=host_ip, content=msg)
    try:
        new_yml = create_ip_yml(task_log)
    except Exception, e:
        data.update({'status': 3, 'status_name': "部署失败"})
        msg = '生成yml文件失败, {error_msg}'.format(error_msg=e)
        content.append(msg)
        print '主机{host_ip}{msg}'.format(host_ip=host_ip, msg=msg)

    try:
        step_count = yml_step_count(new_yml)
    except Exception, e:
        data.update({'status': 3, 'status_name': "部署失败"})
        msg = '记录yml文件步骤失败, {error_msg}'.format(error_msg=e)
        content.append(msg)
        print '主机{host_ip}{msg}'.format(host_ip=host_ip, msg=msg)

    try:
        _playbook_api(task_log.id, new_yml, params)
        data.update({'status': 1, 'status_name': "正在部署"})
        msg = '调用{playbook_name} playbook成功!'.format(playbook_name=playbook_name)
        content.append(msg)
        print '主机{host_ip}{msg}'.format(host_ip=host_ip, msg=msg)

        msg = '正在获取{playbook_name} playbook运行结果......'.format(playbook_name=playbook_name)
        content.append(msg)
        print '主机{host_ip}{msg}'.format(host_ip=host_ip, msg=msg)
    except Exception, e:
        data.update({'status': 3, 'status_name': "部署失败"})
        msg = '调用{playbook_name} playbook失败, {error_msg}'.format(playbook_name=playbook_name, error_msg=e)
        content.append(msg)
        print '主机{host_ip}{content}'.format(host_ip=host_ip, content=msg)
    TaskLog.objects.filter(id=task_log.id).update(status=data['status'], content=','.join(content),
                                                  begin_deploy_at=datetime.now(), step_count=step_count)


@ext_helper.thread_method
def _get_deploy_result(task, task_log, data):
    playbook_name = task_log.role_manage.playbook_name
    content = task_log.content.split(',')

    # 判断是否超时
    # use_time = (datetime.now() - task_log.begin_deploy_at).seconds
    # if use_time > task_log.timeout:
    if task_log.timeout == 0:
        data.update({'status': 3, 'status_name': u"部署失败"})
        msg = u'{playbook_name} playbook运行超时!'.format(playbook_name=playbook_name)
        content.append(msg)
        print '主机{host_ip}部署{playbook_name} playbook运行超时!'.format(host_ip=task_log.host.ip,
                                                                  playbook_name=playbook_name)
    else:
        task_result = task_log.task_result_set.all()
        last_task_result = task_result.last()
        # 如果结果记录数和playbook任务数相同,则说明playbook运行完成
        if len(task_result) == task_log.step_count:
            if last_task_result and last_task_result.ansible_status in ['ok', 'changed']:
                data.update({'status': 2, 'status_name': u"部署成功"})
                print '主机{host_ip}部署任务结束, {playbook_name}部署成功。'.format(host_ip=task_log.host.ip,
                                                                       playbook_name=playbook_name)
            else:
                data.update({'status': 3, 'status_name': u"部署失败"})
                print '主机{host_ip}部署任务结束, {playbook_name}部署失败。'.format(host_ip=task_log.host.ip,
                                                                       playbook_name=playbook_name)
            msg = u'{playbook_name} {status_name}'.format(playbook_name=playbook_name, status_name=data['status_name'])
            content.append(msg)

        else:
            # 如果没完成, 判断是否中途失败
            if last_task_result and last_task_result.task_is_failed():
                data.update({'status': 3, 'status_name': u"部署失败"})
                msg = u'{playbook_name} {status_name}'.format(playbook_name=playbook_name,
                                                              status_name=data['status_name'])
                content.append(msg)
                print '主机{host_ip}部署任务结束, {playbook_name}部署失败。'.format(host_ip=task_log.host.ip,
                                                                       playbook_name=playbook_name)
            else:
                key = '{tid}-{ip}'.format(tid=task_log.id, ip=task_log.host.ip)
                rs_data = redis_api.Rs.lpop(key)
                # print '从Redis中获取{key}的值为{rs_data}'.format(key=key, rs_data=rs_data)
                if rs_data:
                    result = json.loads(rs_data)
                    # print "解析从Redis中获取的json数据,解析结果为{result}".format(result=result)
                    ansible_status = result.get('ansible_status', None)
                    # print "任务结果状态为:{ansible_status}".format(ansible_status=ansible_status)
                    if ansible_status:
                        if ansible_status not in ['ok', 'changed', 'skipped']:
                            data.update({'status': 3, 'status_name': u"部署失败"})
                        Task_Result.objects.create(**result)
    TaskLog.objects.filter(id=task_log.id).update(status=data['status'], content=','.join(content))


# 根据ip生成对应的yml文件
def create_ip_yml(task_log):
    host_ip = task_log.host.ip
    playbook = task_log.role_manage.playbook
    yaml_path = os.path.join(settings.ANSIBLE_YAMLS, playbook)
    with open(yaml_path, 'r+') as f:
        config, ind, bsi = load_yaml_guess_indent(f)
        config[0]['hosts'] = str(host_ip)

    yml_name = str(host_ip).replace('.', '_')
    new_yml = "{name}.yml".format(name=yml_name)
    tmp_ansible_yml = os.path.join(settings.ANSIBLE_YAMLS, new_yml)
    with open(tmp_ansible_yml, 'w') as f:
        ruamel.yaml.round_trip_dump(config, f, indent=ind, block_seq_indent=bsi)
    return tmp_ansible_yml


def yml_step_count(yml_path):
    # 获取yml文件的步骤数
    with open(yml_path, 'r+') as f:
        data = yaml.load(f)
        roles = data[0].get('roles', None)
        step_count = 0
        if roles:
            for role in roles:
                role_yaml_path = os.path.join(settings.ANSIBLE_YAMLS, 'roles', role, 'tasks/main.yml')
                with open(role_yaml_path, 'r+') as rf:
                    step_count += len(yaml.load(rf))
        else:
            tasks = data[0].get('tasks', None)
            step_count += len(tasks)
    return step_count


# 调用playbook_api 接口
@ext_helper.thread_method
def _playbook_api(tid, yml_path, params):
    yaml_list = [str(yml_path)]
    # 将params插入到额外变量
    extra_vars = params
    code = ansible_playbook_api.api(tid, yaml_list, extra_vars)
    if os.path.exists(yml_path):
        os.remove(yml_path)

        # retry_yml = "{name}.retry".format(name=yml_name)
        # tmp_retry_yml = os.path.join(settings.ANSIBLE_YAMLS, retry_yml)
        # if os.path.exists(tmp_ansible_yml):
        #     os.remove(tmp_ansible_yml)

# 重新部署
@transaction.atomic
def retry_deploy(request, id):
    id = ext_helper.to_int(id)
    tid = request.session.get('tid')
    task_logs = TaskLog.objects.filter(pk=id)
    request.session['tid'] = task_logs[0].task_id
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
        task_logs[0].task_result_set.all().delete()
        # 重试清除
        key = '{tid}-{ip}'.format(tid=task_logs[0].id, ip=task_logs[0].host.ip)
        redis_api.Rs.delete(key)
        msg = "success"
    except Exception, e:
        msg = e.message
    task_log = TaskLog.objects.get(pk=id)
    return HttpResponse(json.dumps({'msg': msg, 'status_name': task_log.status_name()}),
                        content_type='application/json')


# 实时更新剩余时间
def update_rest_time(request, id):
    id = ext_helper.to_int(id)
    task_logs = TaskLog.objects.filter(pk=id)
    status = task_logs[0].status
    timeout = task_logs[0].timeout
    # 只有正在部署的时间才会递减
    if status == 1:
        if timeout != 0:
            timeout = timeout - 1
            task_logs.update(timeout=timeout)
    msg = time.strftime('%H:%M:%S', time.gmtime(timeout))
    return HttpResponse(json.dumps({'msg': msg}), content_type='application/json')


def _title_name():
    return '部署明细'


def _class_name():
    return 'task_log'

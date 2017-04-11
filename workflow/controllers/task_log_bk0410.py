#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.db import transaction
from workflow.controllers import *
from workflow.models import Task, TaskLog, HomeWork, RoleManage, Task_Result
import threading

L = threading.Lock()  # 引入锁


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


def ws_get_deploy_result(task_log_id, ip):
    task_log_id = ext_helper.to_int(task_log_id)
    redis_key_info = "{tid}-{ip}-info".format(tid=task_log_id, ip=ip)
    redis_key_result = "{tid}-{ip}-result".format(tid=task_log_id, ip=ip)
    try:
        L.acquire()  # 加锁
        main(task_log_id, redis_key_info, redis_key_result)
        L.release()  # 释放锁
        send_data = {
            'id': task_log_id,
            'status': _get_redis_value(redis_key_info, 'status'),
            'status_name': _get_redis_value(redis_key_info, 'status_name'),
            'use_time': _get_redis_value(redis_key_info, 'use_time'),
            'ws_state': 'success',
            'ws_msg': 'websocket访问服务端正常。'
        }
    except Exception, e:
        print e
        redis_api.Rs.hmset(redis_key_info, {'status': 4, 'status_name': "部署失败"})
        send_data = {
            'id': task_log_id,
            'status': 4,
            'status_name': '部署失败',
            'ws_state': 'error',
            'ws_msg': '服务端异常,请解决异常后继续部署!'}
    return json.dumps(send_data)


@ext_helper.thread_method
def main(task_log_id, redis_key_info, redis_key_result):
    status = _get_redis_value(redis_key_info, 'status')
    rs_content = _get_redis_value(redis_key_info, 'content')
    # 该任务的redis数据字典
    options = redis_api.Rs.hgetall(redis_key_info)

    data = {}
    # 状态-待部署
    if status == "0":
        content_list = _set_deploy(redis_key_info, options)
        content = ','.join(content_list)
        redis_api.Rs.hset(redis_key_info, 'content', content)
        data['step_count'] = _get_redis_value(redis_key_info, 'step_count')
        data['begin_deploy_at'] = datetime.now()
        data['content'] = content

    # 状态-正在部署
    if status == "1":
        content_list = _get_deploy_result(redis_key_info, redis_key_result, options)
        if content_list:
            content = ','.join(content_list)
            rs_content = rs_content + ',' + content
            redis_api.Rs.hset(redis_key_info, 'content', content)
            data['content'] = rs_content

    data['status'] = _get_redis_value(redis_key_info, 'status')
    data['timeout'] = _get_redis_value(redis_key_info, 'use_time')

    # 保存结果数据
    TaskLog.objects.filter(id=task_log_id).update(**data)

    # 删除redis缓存
    # if data['status'] == '2':
    #     redis_api.Rs.delete(redis_key_info, redis_key_result)


# 待部署的状态
def _set_deploy(r_key_info, options):
    id = ext_helper.to_int(options['id'])
    host_ip = options['host_ip']
    params_json = options['params']
    role_name = options['role_name']
    playbook = options['playbook']
    playbook_name = options['playbook_name']
    # 如果事pre_install 角色,切换ubuntu用户
    params = json.loads(params_json)
    if role_name == 'pre_install':
        params['ansible_ssh_user'] = settings.ANSIBLE_INIT_USER
        params['ansible_ssh_pass'] = settings.ANSIBLE_INIT_PASS

    content = []
    msg = '开始安装部署{playbook_name}......'.format(playbook_name=playbook_name)
    content.append(msg)
    print '主机{host_ip}{msg}'.format(host_ip=host_ip, msg=msg)

    # 生成yml文件
    print "主机{host_ip}开始生成yml文件".format(host_ip=host_ip)
    new_yml = _create_ip_yml(host_ip, playbook)
    if not new_yml:
        redis_api.Rs.hmset(r_key_info, {'status': 3, 'status_name': "部署失败"})
        msg = '生成yml文件失败。'
        content.append(msg)
        return content

    # 统计yml文件中任务步骤
    print "主机{host_ip}开始统计yml文件中步骤数".format(host_ip=host_ip)
    step_count = _yml_step_count(host_ip, new_yml)
    if step_count:
        redis_api.Rs.hmset(r_key_info, {'step_count': step_count})
    else:
        redis_api.Rs.hmset(r_key_info, {'status': 3, 'status_name': "部署失败"})
        msg = '计算yml文件步骤失败。'
        content.append(msg)
        return content

    tid = ext_helper.to_int(id)
    resule_code = _playbook_api(tid, new_yml, params, host_ip)
    if resule_code:
        redis_api.Rs.hmset(r_key_info, {'status': 1, 'status_name': "正在部署"})
        msg = '调用{playbook_name} playbook成功!'.format(playbook_name=playbook_name)
        content.append(msg)
        print '主机{host_ip}{msg}'.format(host_ip=host_ip, msg=msg)

        msg = '正在获取{playbook_name} playbook运行结果......'.format(playbook_name=playbook_name)
        content.append(msg)
        print '主机{host_ip}{msg}'.format(host_ip=host_ip, msg=msg)
    else:
        redis_api.Rs.hmset(r_key_info, {'status': 3, 'status_name': "部署失败"})
        msg = '调用{playbook_name} playbook失败'.format(playbook_name=playbook_name)
        content.append(msg)
    return content


# @ext_helper.thread_method
def _get_deploy_result(r_key_info, r_key_result, options):
    host_ip = options['host_ip']
    playbook_name = options['playbook_name']
    timeout = ext_helper.to_int(options['timeout'])
    use_time = ext_helper.to_int(options['use_time'])
    step_count = ext_helper.to_int(options['step_count'])
    current_count = ext_helper.to_int(options['current_step'])

    content = []
    if use_time >= timeout:
        redis_api.Rs.hmset(r_key_info, {'status': 3, 'status_name': "部署失败"})
        msg = '{playbook_name} playbook运行超时!'.format(playbook_name=playbook_name)
        content.append(msg)
    else:
        # 获取结果
        rs_result = redis_api.Rs.lrange(r_key_result, 0, -1)
        if rs_result:
            rs_data = rs_result[0]
            result = json.loads(rs_data)
            redis_api.Rs.hincrby(r_key_info, 'current_step', 1)
            ansible_status = result.get('ansible_status', None)
            # 如果部署完成
            if step_count == current_count + 1:
                if ansible_status in ['ok', 'changed', 'skipped']:
                    redis_api.Rs.hmset(r_key_info, {'status': 2, 'status_name': "部署成功"})
                    msg = '{playbook_name}部署成功。'.format(playbook_name=playbook_name)
                    content.append(msg)
                    print '主机{host_ip}部署任务结束, {playbook_name}部署成功。'.format(host_ip=host_ip, playbook_name=playbook_name)
                else:
                    redis_api.Rs.hmset(r_key_info, {'status': 3, 'status_name': "部署失败"})
                    msg = '{playbook_name}部署失败。'.format(playbook_name=playbook_name)
                    content.append(msg)
                    print '主机{host_ip}部署任务结束, {playbook_name}部署失败。'.format(host_ip=host_ip, playbook_name=playbook_name)
            else:
                if ansible_status not in ['ok', 'changed', 'skipped']:
                    redis_api.Rs.hmset(r_key_info, {'status': 3, 'status_name': "部署失败"})
                    msg = '{playbook_name}部署失败。'.format(playbook_name=playbook_name)
                    content.append(msg)
                    print '主机{host_ip}部署任务结束, {playbook_name}部署失败。'.format(host_ip=host_ip, playbook_name=playbook_name)

            try:
                Task_Result.objects.create(**result)
            except Exception, e:
                print "主机{host_ip}存储ansible结果异常。".format(host_ip=host_ip)
                print e
            else:
                redis_api.Rs.lpop(r_key_result)
    return content


# 根据ip生成对应的yml文件
def _create_ip_yml(host_ip, playbook):
    try:
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
    except Exception, e:
        print '主机{host_ip}生成yml文件失败,{error_msg}'.format(host_ip=host_ip, error_msg=e)
        return None


# 统计yml文件中任务步骤
def _yml_step_count(host_ip, yml_path):
    try:
        with open(yml_path, 'r+') as f:
            data = yaml.load(f)
            roles = data[0].get('roles', None)
            step_count = 0
            if roles:
                for role in roles:
                    role_yaml_path = os.path.join(settings.ANSIBLE_YAMLS, 'roles', role, 'tasks/main.yml')
                    with open(role_yaml_path, 'r+') as rf:
                        for d in yaml.load(rf):
                            if d.get('name', None):
                                step_count += 1
            else:
                tasks = data[0].get('tasks', None)
                for d in tasks:
                    if d.get('name', None):
                        step_count += 1
        return step_count
    except Exception, e:
        print '主机{host_ip}生成yml文件失败,{error_msg}'.format(host_ip=host_ip, error_msg=e)
        return None


# 调用playbook_api 接口
# @ext_helper.thread_method
def _playbook_api(tid, yml_path, params, host_ip):
    try:
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
        return True
    except Exception, e:
        print '主机{host_ip}调用playbook接口失败, {error_msg}'.format(host_ip=host_ip, error_msg=e)
        return False


# 重新部署
@transaction.atomic
def retry_deploy(request, id):
    id = ext_helper.to_int(id)
    tid = request.session.get('tid')
    task_logs = TaskLog.objects.filter(pk=id)
    task_log = task_logs[0]
    request.session['tid'] = task_log.task_id
    try:
        # 事务处理
        task_logs.update(
            content="",
            status=0,
            ansible_status="",
            begin_deploy_at=datetime.now(),
            timeout=task_log.role_manage.timeout
        )
        Task.objects.filter(id=tid).update(status=1)
        task_log.task_result_set.all().delete()
        # 重试清除
        redis_api.Rs.delete(task_log.redis_key_result())
        redis_api.Rs.hmset(task_log.redis_key_info(), {
            'status': 0,
            'status_name': "待部署",
            'use_time': 0,
            'current_step': 0,
            'content': ''})
        msg = "success"
    except Exception, e:
        print e
        msg = "error"
    return HttpResponse(json.dumps({'msg': msg, 'status_name': "待部署"}),
                        content_type='application/json')


# 实时更新剩余时间
def update_rest_time(request, key):
    # 当redis缓存先被清除后, 则停止前端时间刷新
    # if not redis_api.Rs.hexists(key):
    #     state = 'stop'
    #     msg = ''
    #     return HttpResponse(json.dumps({'state': state, 'msg': msg}), content_type='application/json')
    # else:
    try:
        redis_api.Rs.hincrby(key, 'use_time')
        timeout = redis_api.Rs.hget(key, 'timeout')
        use_time = redis_api.Rs.hget(key, 'use_time')
        real_time = int(timeout) - int(use_time)
        if real_time < 0:
            raise
        state = "success"
        msg = time.strftime('%H:%M:%S', time.gmtime(real_time))
    except Exception, e:
        print "{key}的剩余时间更新异常, 请处理异常后继续完成部署。".format(key=key)
        print e.message
        state = "error"
        msg = "{key}的剩余时间更新异常, 请处理异常后继续完成部署。".format(key=key)
    return HttpResponse(json.dumps({'state': state, 'msg': msg}), content_type='application/json')


def _get_redis_value(key, field):
    try:
        return redis_api.Rs.hget(key, field)
    except Exception, e:
        return None


def _deploy_failed(r_key_info, error_msg):
    redis_api.Rs.hmset(r_key_info, {'status': 3, 'status_name': "部署失败"})
    print error_msg
    return False


def _title_name():
    return '部署明细'


def _class_name():
    return 'task_log'

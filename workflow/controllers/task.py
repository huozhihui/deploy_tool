#!/usr/bin/python
# -*- coding: utf-8 -*-
from workflow.controllers import *
from workflow.models import Task, TaskLog


def index(request):
    title_name = _title_name()
    class_name = _class_name()
    msg = ext_helper.get_msg(request)
    object_list = ext_helper.get_objects(request, 'Task')
    tid = request.session.get('tid', None)
    render_url = "%s/%s" % (_class_name(), 'index.html')
    return render_to_response(render_url, locals())


def delete(request, id):
    id = ext_helper.to_int(id)
    tid = request.session.get('tid', None)
    obj = Task.objects.get(pk=id)
    task_logs = obj.tasklog_set.all()
    obj.delete()
    if obj.id:
        request.session['msg'] = "数据删除失败!"
        # 清除该任务的redis缓存
        for task_log in task_logs:
            print task_log
            print task_log.redis_key_info()
            print task_log.redis_key_result()
            redis_api.Rs.delete(task_log.redis_key_info(), task_log.redis_key_result())
    else:
        # 如果清除的是当前的任务,则清除session
        if id == tid:
            ext_helper.del_session(request, 'tid')
        request.session['msg'] = "数据删除成功!"
    return index(request)


def continue_deploy(request, id):
    id = ext_helper.to_int(id)
    request.session['tid'] = id
    return HttpResponseRedirect("/homework/confirm_deploy")


def set_task_complete(request):
    print "更新任务状态"
    try:
        tid = request.session.get('tid', None)
        task = Task.objects.get(pk=tid)
        if task.is_completed():
            Task.objects.filter(id=tid).update(status=2)
            ext_helper.del_session(request, 'tid')
            msg = 'Update Task status Successfully'
        else:
            msg = 'Task not deploy over!'
    except Exception, e:
        msg = 'Warn: task update error!'
    return HttpResponse(json.dumps({'msg': msg}), content_type='application/json')


def _title_name():
    return '部署纪录'


def _class_name():
    return 'task'

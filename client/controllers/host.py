#!/usr/bin/python
# -*- coding: utf-8 -*-
from client.forms import HostForm
from client.models import Host, RoleManage, Host_Role
from client.controllers import *

def index(request):
    title_name = _title_name()
    class_name = _class_name()
    msg = ext_helper.get_msg(request)
    object_list = ext_helper.get_objects(request, class_name.title())
    render_url = "%s/%s" % (_class_name(), 'index.html')
    return render_to_response(render_url, locals())


def new(request):
    title_name = _title_name()
    class_name = _class_name()
    role_manages = RoleManage.objects.filter(user_id=request.user.id)
    operation = "添加"
    if request.method == 'POST':  # 当提交表单时
        instance, msg= ext_helper.create_date(request, 'Host', 'ip')
        role_ids = request.POST.getlist('role_ids')
        for role_id in role_ids:
            Host_Role.objects.create(host_id=instance.id, role_manage_id=role_id, user_id=request.user.id)
    form = HostForm(initial={'port': 22})
    return render(request, 'host/form.html', locals())


def dialog_new(request):
    dialog_title = "添加节点"
    if request.method == 'GET':
        role_manages = RoleManage.objects.filter(user_id=request.user.id)
        form_url = '/%s/%s' % (_class_name(), 'dialog_new')
        form = HostForm(initial={'host_group': 1, 'port': 22})
        return render(request, 'host/dialog_form.html', locals())
    else:
        host_role_list = request.POST.getlist('host_roles')
        d = {'host_roles': ','.join(host_role_list)}
        instance, msg = ext_helper.create_date(request, 'Host', 'ip', d)
        request.session['msg'] = msg
        return index(request)

def edit(request, id):
    id = ext_helper.to_int(id)
    title_name = _title_name()
    class_name = _class_name()
    operation = "编辑"
    role_manages = RoleManage.objects.filter(user_id=request.user.id)
    if request.method == 'POST':  # 当提交表单时
        result_status, msg = ext_helper.update_date(request, id, 'Host', 'ip')
        Host_Role.objects.filter(host_id=id).delete()
        role_ids = request.POST.getlist('role_ids')
        for role_id in role_ids:
            Host_Role.objects.create(host_id=id, role_manage_id=role_id, user_id=request.user.id)

        request.session['msg'] = msg
        if result_status:
            return index(request)
        else:
            return render(request, 'host/form.html', locals())
    else:
        host = Host.objects.get(pk=id)
        select_role_list = host.host_role_set.all().values_list('role_manage_id', flat=True)
        select_role =  '_'.join(map(str, list(select_role_list)))
        form = HostForm(instance=host)
        return render(request, 'host/form.html', locals())


def delete(request, id):
    id = ext_helper.to_int(id)
    obj = Host.objects.get(pk=id)
    obj.delete()
    if obj.id:
        request.session['msg'] = "数据删除失败!"
    else:
        request.session['msg'] = "数据删除成功!"
    return index(request)


def ajax_valid_ip(request):
    ip = request.GET['ip']
    try:
        Host.objects.get(ip=ip)
        msg = "{ip}已存在。".format(ip=ip)
    except:
        msg = ''
    return HttpResponse(json.dumps({'msg': msg}), content_type='application/json')


def _title_name():
    return '节点'


def _class_name():
    return 'host'

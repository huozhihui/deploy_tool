#!/usr/bin/python
# -*- coding: utf-8 -*-
from client.forms import DynamicVarForm
from client.models import DynamicVar
from client.controllers import *

def index(request):
    title_name = _title_name()
    class_name = _class_name()
    msg = ext_helper.get_msg(request)
    object_list = ext_helper.get_objects(request, 'DynamicVar')
    render_url = "%s/%s" % (_class_name(), 'index.html')
    return render_to_response(render_url, locals())


def new(request):
    title_name = _title_name()
    class_name = _class_name()
    operation = "添加"
    if request.method == 'POST':  # 当提交表单时
        instance, msg= ext_helper.create_date(request, 'DynamicVar', 'name')
    form = DynamicVarForm()
    return render(request, 'dynamic_var/form.html', locals())


def edit(request, id):
    id = ext_helper.to_int(id)
    title_name = _title_name()
    class_name = _class_name()
    operation = "编辑"
    if request.method == 'POST':  # 当提交表单时
        result_status, msg = ext_helper.update_date(request, id, 'DynamicVar', 'name')
        request.session['msg'] = msg
        if result_status:
            return index(request)
        else:
            return render(request, 'dynamic_var/form.html', locals())
    else:
        host = DynamicVar.objects.get(pk=id)
        form = DynamicVarForm(instance=host)
        return render(request, 'dynamic_var/form.html', locals())


def delete(request, id):
    id = ext_helper.to_int(id)
    obj = DynamicVar.objects.get(pk=id)
    obj.delete()
    if obj.id:
        request.session['msg'] = "数据删除失败!"
    else:
        request.session['msg'] = "数据删除成功!"
    return index(request)

# 校验名称唯一性
def ajax_valid_name(request):
    name = request.GET['name']
    try:
        role_manage = DynamicVar.objects.get(name=name)
        msg = "{name}已存在。".format(name=name)
    except:
        msg = ''
    return HttpResponse(json.dumps({'msg': msg}), content_type='application/json')


def _title_name():
    return '变量'


def _class_name():
    return 'dynamic_var'

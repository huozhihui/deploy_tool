#!/usr/bin/python
# -*- coding: utf-8 -*-
from client.controllers import *
from client.forms import HostGroupForm
from client.models import HostGroup



def index(request):
    title_name = _title_name()
    class_name = _class_name()
    msg = ext_helper.get_msg(request)
    object_list = ext_helper.get_objects(request, 'HostGroup')
    render_url = "%s/%s" % (_class_name(), 'index.html')
    return render_to_response(render_url, locals())


def new(request):
    title_name = _title_name()
    class_name = _class_name()
    operation = "添加"
    if request.method == 'POST':  # 当提交表单时
        form = HostGroupForm(request.POST)  # form 包含提交的数据
        if form.is_valid():  # 如果提交的数据合法
            name = form.cleaned_data['name']
            describe = form.cleaned_data['describe'] or name
            user_id = request.user.id
            obj = HostGroup(name=name, describe=describe, user_id=user_id)
            obj.save()
            if obj.id:
                msg = u"%s 添加成功!" % name
            else:
                msg = u"%s 添加失败!" % name
    form = HostGroupForm()
    return render(request, 'host_group/form.html', locals())


def edit(request, id):
    id = ext_helper.to_int(id)
    title_name = _title_name()
    class_name = _class_name()
    operation = "编辑"
    if request.method == 'POST':  # 当提交表单时
        form = HostGroupForm(request.POST)  # form 包含提交的数据
        if form.is_valid():  # 如果提交的数据合法
            name = form.cleaned_data['name']
            describe = form.cleaned_data['describe'] or name
            user_id = request.user.id
            if HostGroup.objects.filter(pk=id).update(name=name, describe=describe, user_id=user_id):
                msg = u"%s 编辑成功!" % name
                return index(request)
            else:
                msg = u"%s 编辑失败!" % name
                return render(request, 'host_group/form.html', locals())
    else:
        host_group = HostGroup.objects.get(pk=id)
        form = HostGroupForm(instance=host_group)
        return render(request, 'host_group/form.html', locals())


def delete(request, id):
    id = ext_helper.to_int(id)
    obj = HostGroup.objects.get(pk=id)
    obj.delete()
    if obj.id:
        request.session['msg'] = "数据删除失败!"
    else:
        request.session['msg'] = "数据删除成功!"
    return index(request)


def _title_name():
    return '客户端组'


def _class_name():
    return 'host_group'

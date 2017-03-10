#!/usr/bin/python
# -*- coding: utf-8 -*-
from client.controllers import *
from client.forms import RoleManageForm
from client.models import RoleManage, DynamicVar


def index(request):
    title_name = _title_name()
    class_name = _class_name()
    msg = ext_helper.get_msg(request)
    object_list = ext_helper.get_objects(request, 'RoleManage')
    render_url = "%s/%s" % (_class_name(), 'index.html')
    return render_to_response(render_url, locals())


def new(request):
    title_name = _title_name()
    class_name = _class_name()
    operation = "添加"
    playbook_list = _playbook_list()
    dynamic_vars = DynamicVar.objects.all()
    if request.method == 'POST':  # 当提交表单时
        dynamic_var_list = request.POST.getlist('dynamic_vars')
        d = {'dynamic_vars': ','.join(dynamic_var_list), 'playbook': request.POST['playbook']}
        instance, msg = ext_helper.create_date(request, 'RoleManage', 'name', d)
    form = RoleManageForm()
    return render(request, 'role_manage/form.html', locals())


def edit(request, id):
    id = ext_helper.to_int(id)
    title_name = _title_name()
    class_name = _class_name()
    operation = "编辑"
    playbook_list = _playbook_list()
    dynamic_vars = DynamicVar.objects.all()
    role_manage = get_object_or_404(RoleManage, pk=id)
    if request.method == 'POST':
        dynamic_var_list = request.POST.getlist('dynamic_vars')
        d = {'dynamic_vars': ','.join(dynamic_var_list), 'playbook': request.POST['playbook']}
        result_status, msg = ext_helper.update_date(request, id, 'RoleManage', 'name', d)
        request.session['msg'] = msg
        if result_status:
            return index(request)
        else:
            return render(request, 'role_manage/form.html', locals())

    # if request.method == 'POST':
    #     form = RoleManageForm(request.POST, instance=role_manage)
    #     if form.is_valid():
    #         form.save()
    #         msg = u"%s 编辑成功!" % role_manage.name
    #         request.session['msg'] = msg
    #         return index(request)
    #     else:
    #         msg = form.errors
    #         return render(request, 'role_manage/form.html', locals())
    else:
        form = RoleManageForm(instance=role_manage)
        return render(request, 'role_manage/form.html', locals())


def delete(request, id):
    id = ext_helper.to_int(id)
    obj = RoleManage.objects.get(pk=id)
    obj.delete()
    if obj.id:
        request.session['msg'] = "数据删除失败!"
    else:
        request.session['msg'] = "数据删除成功!"
    return index(request)


def _title_name():
    return '角色'


def _class_name():
    return 'role_manage'


def _playbook_list():
    playbook_list = []
    roles_path = settings.ANSIBLE_YAMLS
    for file in os.listdir(roles_path):
        if file.endswith(".yaml") or file.endswith(".yml"):
            playbook_list.append(file)

        # pb_install = os.path.join(roles_path, file)
        # if os.path.isdir(pb_install):
        #     main_file = os.path.join(pb_install, 'tasks', 'main.yaml')
        #     # 如果main.yaml文件存在,则页面显示该应用
        #     if os.path.exists(main_file):
        #         playbook_list.append(file)
    return playbook_list




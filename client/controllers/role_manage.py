#!/usr/bin/python
# -*- coding: utf-8 -*-
from client.controllers import *
from client.forms import RoleManageForm
from client.models import RoleManage, DynamicVar, Role_Dynamic_Variable


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
        instance, msg = ext_helper.create_date(request, 'RoleManage', 'name', _post_data(request))
        dynamic_var_ids = request.POST.getlist('dynamic_vars')
        for dynamic_var_id in dynamic_var_ids:
            Role_Dynamic_Variable.objects.create(dynamic_var_id=dynamic_var_id, role_manage_id=instance.id,
                                                 user_id=request.user.id)

    count = ext_helper.get_objects(request, 'RoleManage').count()
    form = RoleManageForm(initial={'num': count + 1})
    return render(request, 'role_manage/form.html', locals())


def edit(request, id):
    id = ext_helper.to_int(id)
    title_name = _title_name()
    class_name = _class_name()
    operation = "编辑"
    playbook_list = _playbook_list()
    # 页面显示所有的动态参数
    dynamic_vars = DynamicVar.objects.all()
    role_manage = get_object_or_404(RoleManage, pk=id)

    if request.method == 'POST':
        result_status, msg = ext_helper.update_date(request, id, 'RoleManage', 'name', _post_data(request))
        request.session['msg'] = msg

        Role_Dynamic_Variable.objects.filter(user_id=request.user.id, role_manage_id=id).delete()
        dynamic_var_ids = request.POST.getlist('dynamic_vars')
        for dynamic_var_id in dynamic_var_ids:
            Role_Dynamic_Variable.objects.create(dynamic_var_id=dynamic_var_id, role_manage_id=id,
                                                 user_id=request.user.id)
        if result_status:
            return index(request)
        else:
            return render(request, 'role_manage/form.html', locals())

    else:
        form = RoleManageForm(instance=role_manage)
        return render(request, 'role_manage/form.html', locals())


# 记录yml文件步骤
def _post_data(request):
    playbook = request.POST['playbook']
    playbook_name = playbook.split('.')[0]
    # playbook_path = os.path.join(settings.ANSIBLE_YAMLS, playbook)
    # with open(playbook_path, 'r+') as f:
    #     data = yaml.load(f)
    #     roles = data[0].get('roles', None)
    #     step_count = 0
    #     if roles:
    #         for role in roles:
    #             role_yaml_path = os.path.join(settings.ANSIBLE_YAMLS, 'roles', role, 'tasks/main.yml')
    #             with open(role_yaml_path, 'r+') as rf:
    #                 step_count += len(yaml.load(rf))
    #     else:
    #         tasks = data[0].get('tasks', None)
    #         step_count += len(tasks)
    # return {'playbook': playbook, 'playbook_name': playbook_name, 'step_count': step_count}
    return {'playbook': playbook, 'playbook_name': playbook_name}


def delete(request, id):
    id = ext_helper.to_int(id)
    obj = RoleManage.objects.get(pk=id)
    obj.delete()
    if obj.id:
        request.session['msg'] = "数据删除失败!"
    else:
        request.session['msg'] = "数据删除成功!"
    return index(request)


def ajax_valid_name(request):
    name = request.GET['name']
    try:
        role_manage = RoleManage.objects.get(name=name)
        msg = "{name}已存在。".format(name=name)
    except:
        msg = ''
    print msg
    return HttpResponse(json.dumps({'msg': msg}), content_type='application/json')


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

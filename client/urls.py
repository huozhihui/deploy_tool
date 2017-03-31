from django.conf.urls import url
from django.contrib.auth.decorators import login_required

# import views
from client.controllers import *

# app_name = 'client'
urlpatterns = [
    # url(r'^index', login_required(views.HostListView.as_view()), name='host-list'),
    # url(r'^new', login_required(views.HostCreate.as_view()), name='host-new'),
    url(r'^host$', login_required(host.index), name='host'),
    url(r'^host/new', login_required(host.new), name='host_new'),
    url(r'^host/dialog_new', login_required(host.dialog_new), name='host_dialog_new'),
    url(r'^host/edit/(\d{1,8})$', login_required(host.edit), name='host_edit'),
    url(r'^host/delete/(\d{1,8})$', login_required(host.delete), name='host_delete'),
    url(r'^host/ajax_valid_ip$', login_required(host.ajax_valid_ip),
        name='host_ajax_valid_ip'),

    url(r'^host_group$', login_required(host_group.index), name='host_group_index'),
    url(r'^host_group/new', login_required(host_group.new), name='host_group_new'),
    url(r'^host_group/edit/(\d{1,8})$', login_required(host_group.edit), name='host_group_edit'),
    url(r'^host_group/delete/(\d{1,8})$', login_required(host_group.delete), name='host_group_delete'),

    url(r'^$', login_required(role_manage.index), name='role_manage_index'),
    url(r'^role_manage$', login_required(role_manage.index), name='role_manage_index'),
    url(r'^role_manage/new', login_required(role_manage.new), name='role_manage_new'),
    url(r'^role_manage/edit/(\d{1,8})$', login_required(role_manage.edit), name='role_manage_edit'),
    url(r'^role_manage/delete/(\d{1,8})$', login_required(role_manage.delete), name='role_manage_delete'),
    url(r'^role_manage/ajax_valid_name$', login_required(role_manage.ajax_valid_name),
        name='role_manage_ajax_valid_name'),

    url(r'^dynamic_var$', login_required(dynamic_var.index), name='dynamic_var_index'),
    url(r'^dynamic_var/new', login_required(dynamic_var.new), name='dynamic_var_new'),
    url(r'^dynamic_var/edit/(\d{1,8})$', login_required(dynamic_var.edit), name='dynamic_var_edit'),
    url(r'^dynamic_var/delete/(\d{1,8})$', login_required(dynamic_var.delete), name='dynamic_var_delete'),
    url(r'^dynamic_var/ajax_valid_name$', login_required(dynamic_var.ajax_valid_name),
        name='dynamic_var_ajax_valid_name'),

    url(r'^user_operate$', login_required(user_operate.index), name='user_operate_index'),
    url(r'^user_operate/get_result$', login_required(user_operate.get_result), name='user_operate_get_result'),

    url(r'^group_operate$', login_required(group_operate.index), name='group_operate_index'),
    url(r'^group_operate/get_result$', login_required(group_operate.get_result), name='group_operate_get_result'),

    url(r'^cmd_operate$', login_required(cmd_operate.index), name='cmd_operate_index'),
    url(r'^cmd_operate/get_result$', login_required(cmd_operate.get_result), name='cmd_operate_get_result'),

    url(r'^file_operate$', login_required(file_operate.index), name='file_operate_index'),
    url(r'^file_operate/get_result$', login_required(file_operate.get_result), name='file_operate_get_result'),

    url(r'^send_file$', login_required(send_file.index), name='send_file_index'),
    url(r'^send_file/get_result$', login_required(send_file.get_result), name='send_file_get_result'),
]

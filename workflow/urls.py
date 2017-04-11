from django.conf.urls import url
from django.contrib.auth.decorators import login_required

import views
from workflow.controllers import *

urlpatterns = [
    # url(r'^index', login_required(views.HostListView.as_view()), name='host-list'),
    # url(r'^new', login_required(views.HostCreate.as_view()), name='host-new'),
    url(r'^homework$', login_required(homework.index), name='homework_index'),
    url(r'^homework/new', login_required(homework.new), name='homework_new'),
    url(r'^homework/edit/(\d{1,8})$', login_required(homework.edit), name='homework_edit'),
    url(r'^homework/delete/(\d{1,8})$', login_required(homework.delete), name='homework_delete'),
    url(r'^homework/select_deploy/(\d{1,8})$', login_required(homework.select_deploy), name='homework_select_deploy'),

    url(r'^homework/select_role$', login_required(homework.select_role), name='homework_select_role'),
    url(r'^homework/confirm_role$', login_required(homework.confirm_role), name='homework_confirm_role'),

    url(r'^homework/select_node$', login_required(homework.select_node), name='homework_select_node'),
    url(r'^homework/confirm_node$', login_required(homework.confirm_node), name='homework_confirm_node'),

    url(r'^homework/config_params/$', login_required(homework.config_params), name='homework_config_params'),
    url(r'^homework/create_params$', login_required(homework.create_params), name='homework_create_params'),
    url(r'^homework/update_params/(\d{1,8})$', login_required(homework.update_params), name='homework_update_params'),
    url(r'^homework/delete_params/(\d{1,8})$', login_required(homework.delete_params), name='homework_delete_params'),

    url(r'^homework/confirm_deploy$', login_required(homework.confirm_deploy), name='homework_confirm_deploy'),
    url(r'^homework/delete_task_log/(\d{1,8})$', login_required(homework.delete_task_log), name='homework_delete_task_log'),

    # url(r'^homework/before_deploy_check$', login_required(homework.before_deploy_check), name='homework_before_deploy_check'),
    url(r'^homework/deploy_status$', login_required(homework.deploy_status), name='homework_deploy_status'),

    # url(r'^homework/get_deploy_result/(\d{1,8})$', login_required(homework.get_deploy_result), name='homework_get_deploy_result'),
    # url(r'^homework/begin_deploy$', login_required(homework.begin_deploy), name='homework_begin_deploy'),
    url(r'^homework/deploy_log/(\d{1,8})$', login_required(homework.deploy_log), name='homework_deploy_log'),

    url(r'^task$', login_required(task.index), name='task_index'),
    url(r'^task/delete/(\d{1,8})$', login_required(task.delete), name='task_delete'),
    url(r'^task/continue_deploy/(\d{1,8})$', login_required(task.continue_deploy), name='task_continue_deploy'),
    url(r'^task/set_task_complete$', login_required(task.set_task_complete), name='task_set_task_complete'),

    url(r'^tlog$', login_required(task_log.index), name='task_log_index'),
    url(r'^task_log/select/(\d{1,8})$', login_required(task_log.select), name='task_log_select'),
    url(r'^task_log/delete/(\d{1,8})$', login_required(task_log.delete), name='task_log_delete'),
    url(r'^task_log/retry_deploy/(\d{1,8})$', login_required(task_log.retry_deploy), name='task_log_retry_deploy'),
    url(r'^task_log/update_rest_time/(?P<key>[\w\-\.]{9,29})$', login_required(task_log.update_rest_time), name='task_log_update_rest_time'),

]
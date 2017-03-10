#!/usr/bin/python
# -*- coding: utf-8 -*-
from client.controllers import *
from client.forms import SendFileForm


def index(request):
    title_name = _title_name()
    class_name = _class_name()
    init_date = {'backup': 'no', 'mode': '0664'}
    form = SendFileForm(initial=init_date)
    object_list = ext_helper.get_objects(request, 'Host')
    render_url = "%s/%s" % (_class_name(), 'index.html')
    # render_url = "base/index.html"
    return render(request, render_url, locals())


def get_result(request):
    if request.method == 'POST':  # 当提交表单时
        form = SendFileForm(request.POST, request.FILES)  # form 包含提交的数据
        if form.is_valid():  # 如果提交的数据合法
            date = request.POST
            tid = ext_helper.generate_tid()
            file_path = _handle_uploaded_file(request.FILES['src'], tid)
            date['src'] = file_path
            _ansible_api(tid, date)
            redis_result = redis_api.RedisResult(tid)
            object_list = redis_result.get_instance()
            # 清除redis任务
            pattern = "{tid}*".format(tid=tid)
            for key in redis_api.Rs.scan_iter(match=pattern):
                redis_api.Rs.delete(key)
            # 清除缓存文件
            shutil.rmtree(os.path.dirname(file_path))
    else:
        error_msg = "Status 400: 错误的请求方式!"
    render_url = "base/_result.html"
    return render(request, render_url, locals())


def _ansible_api(tid, form_date):
    params = {k: v for k, v in form_date.iteritems() if v != ''}
    ext_vars = {"ansible_ssh_user": "root", "ansible_ssh_pass": "root"}

    hosts = form_date['hosts']
    params = {k: v for k, v in params.iteritems() if (k not in ['hosts', 'csrfmiddlewaretoken'])}
    ansible_api.api(tid, 'copy', hosts, params, ext_vars)


def _handle_uploaded_file(f, tid):
    dir = os.path.join(settings.UPLOAD_FILE, tid)
    if not os.path.exists(dir):
        os.mkdir(dir)
    file = os.path.join(dir, f.name)
    with open(file, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return file


def _title_name():
    return '下发文件'


def _class_name():
    return 'send_file'
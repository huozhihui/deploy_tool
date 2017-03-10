#!/usr/bin/python
# -*- coding: utf-8 -*-
import random, datetime
from django.db.models import Q
from threading import Thread
from client.models import *
from client.forms import *
from workflow.models import *
from workflow.forms import *

# 获取访问地址
def base_url(request):
    return request.get_host()


# 获取对象
def get_objects(request, class_name):
    if request.user.is_superuser == 1:
        return eval(class_name).objects.all()
    else:
        return eval(class_name).objects.filter(Q(user_id=request.user.id) | Q(user__is_superuser=1))


def get_user_objects(request, class_name):
    if request.user.is_superuser:
        return eval(class_name).objects.all()
    else:
        return eval(class_name).objects.filter(Q(user_id=request.user.id))

def to_int(id):
    try:
        return int(id)
    except ValueError:
        raise Http404()


def get_msg(request):
    msg = request.session.get('msg', None)
    if msg:
        del request.session['msg']
    return msg


def del_session(request, name):
    if request.session.get(name, None):
        del request.session[name]


# 生成随机码
def generate_random(size):
    if not isinstance(size, int):
        raise ValueError('parameter must be a integer!')
    num='0123456789'
    zm = ''.join({chr(i) for i in range(97, 123)})
    return ''.join(random.sample(list(num+zm), size))

def thread_method(function):
    def decorator(*args, **kwargs):
        t = Thread(target=function, args=args, kwargs=kwargs)
        t.daemon = True
        t.start()

    return decorator

# 生成任务ID
def generate_tid():
    dt = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    rand = random.randint(10, 99)
    return "{dt}-{rand}".format(dt=dt, rand=rand)

def create_date(request, klass, field, options={}):
    instance = None
    klassForm = "%sForm" % klass
    form = eval(klassForm)(request.POST)  # form 包含提交的数据
    if form.is_valid():  # 如果提交的数据合法
        form.cleaned_data['user_id'] = request.user.id
        for k, v in options.items():
            form.cleaned_data[k] = v

        dates = form.cleaned_data
        obj = eval(klass).objects.create(**dates)
        obj.save()
        if obj.id:
            instance = obj
            msg = u"%s 添加成功!" % dates[field]
        else:
            msg = u"%s 添加失败!" % dates[field]
    else:
        msg = form.errors
    return instance, msg

def update_date(request, id, klass, field, options={}):
    result_status = False
    klassForm = "%sForm" % klass
    form = eval(klassForm)(request.POST)  # form 包含提交的数据
    if form.is_valid():  # 如果提交的数据合法
        form.cleaned_data['user_id'] = request.user.id
        for k, v in options.items():
            form.cleaned_data[k] = v

        dates = form.cleaned_data
        if eval(klass).objects.filter(pk=id).update(**dates):
            msg = u"%s 编辑成功!" % dates[field]
            result_status = True
        else:
            msg = u"%s 编辑失败!" % dates[field]
    else:
        msg = form.errors
    return result_status, msg

def delete_date(request, klass, id):
    id = to_int(id)
    obj = eval(klass).objects.get(pk=id)
    obj.delete()
    if obj.id:
        msg = "数据删除失败!"
    else:
        msg = "数据删除成功!"
    return msg





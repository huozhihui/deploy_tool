from django.shortcuts import render, redirect, render_to_response, HttpResponse
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.conf import settings
from common import ansible_api
from common import ext_helper
import os, shutil, re, json, random, yaml
from datetime import datetime
from common import redis_api
import pdb

import host
import user_operate
import group_operate
import cmd_operate
import file_operate
import send_file
import host_group
import role_manage
import dynamic_var

# controller = ['user_operate', 'group_operate', 'cmd_operate', 'file_operate',
#               'send_file', 'host_group', 'role_manage']
# common_module = ['ansible_api', 'ext_helper', 'redis_api']
# other = ['render', 'redirect', 'render_to_response', 'HttpResponseRedirect', 'HttpResponse', 'settings']
# # system_list = ['re', 'os', 'shutil', 'time', 'json', 'timeout_decorator', 'datetime', 'random']
# system_list = ['os', 're', 'shutil', 'json', 'datetime', 'random', 'yaml']
#
# __all__ = controller + common_module + other + system_list
from django.shortcuts import render, redirect, render_to_response, HttpResponse
from django.http import HttpResponseRedirect
from django.conf import settings
from django.db.models import Q
import os, shutil, re, json, random, yaml, pdb, ruamel.yaml
import configparser
from ruamel.yaml.util import load_yaml_guess_indent
import time
from datetime import datetime
import functools
from collections import defaultdict, OrderedDict

from common import ansible_api, ansible_playbook_api
from common import ext_helper
from common import redis_api

import homework
import task
import task_log

# controller = ['homework']
# common_module = ['ansible_api', 'ansible_playbook_api', 'ext_helper', 'redis_api']
# other = ['render', 'redirect', 'render_to_response', 'HttpResponseRedirect', 'HttpResponse', 'settings', 'Q']
# # system_list = ['re', 'os', 'shutil', 'time', 'json', 'timeout_decorator', 'datetime', 'random']
# system_list = ['os', 're', 'shutil', 'json', 'datetime', 'random', 'yaml', 'functools']
#
# __all__ = controller + common_module + other + system_list


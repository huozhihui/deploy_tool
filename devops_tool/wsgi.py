"""
WSGI config for devops_tool project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/howto/deployment/wsgi/
"""
import os
import sys

rootDir = os.path.dirname(os.path.realpath(__file__))
rootDirArr = rootDir.split('/')
rootDirNew = '/'.join(rootDirArr[:len(rootDirArr)-2])

sys.path.append(rootDirNew+'/devops_tool')
sys.path.append(rootDirNew+'/lib/python2.7/site-packages')

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "devops_tool.settings")

application = get_wsgi_application()

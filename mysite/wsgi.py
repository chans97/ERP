"""
WSGI config for mysite project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""


import os
import time
import traceback
import signal
import sys
from django.core.wsgi import get_wsgi_application
from django.core.handlers.wsgi import WSGIHandler

sys.path.append('/opt/bitnami/apps/django/django_projects/cirucs')
os.environ["DJANGO_SETTINGS_MODULE"] = "mysite.settings"
application = get_wsgi_application()

# 파이썬의 절대경로
# sys.path.append("C:/Apache24/htdocs/<PROJECT-ROOT-DIRECTORY>")


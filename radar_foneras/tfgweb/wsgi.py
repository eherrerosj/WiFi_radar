"""
WSGI config for tfgweb project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""
"""
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tfgweb.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
"""

import os, sys
sys.path.append('/srv/Servidor/web/tfgweb')
sys.path.append('/srv/Servidor/web/tfgweb/tfgweb')
sys.path.append('/srv/Servidor/web/tfgweb/tfgplot')
sys.path.append('/usr/local/lib/python2.6/dist-packages/django')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tfgweb.settings")


import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()

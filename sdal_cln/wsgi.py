"""
WSGI config for sdal_cln project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

import environ

root = environ.Path(__file__) - 2
env = environ.Env()
env.read_env(root('.env'))

#os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sdal_cln.settings.dev")
#os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sdal_cln.settings.production")
env('DJANGO_SETTINGS_MODULE', default="sdal_cln.settings.dev")

application = get_wsgi_application()

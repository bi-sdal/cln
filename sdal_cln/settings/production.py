from .base import *
import os
import environ

root = environ.Path(__file__) - 3
env = environ.Env()
env.read_env(root('.env'))

SECRET_KEY = env('SECRET_KEY')
DEBUG = env('DEBUG') == 'True'
print(DEBUG)

print ('USING PRODUCTION')

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres',
        'HOST': 'db',
        'PORT': 5434,
    }
}

try:
    from .local import *
except ImportError:
    pass

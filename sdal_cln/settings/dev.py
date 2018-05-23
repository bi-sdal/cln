from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '=)iv&z7fpx)edffw_ml=*!@0um-#&+$paa@%khmja-g3=()+vl'


EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

print('USING DEV')

try:
    from .local import *
except ImportError:
    pass

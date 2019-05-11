from .base import *

DEBUG = False

DATABASES = {
    'local': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    },
        'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'product',
        'USER': 'product',
        'PASSWORD': '12SDdv@7F?lJ',
        'HOST': 'localhost',
    }

}
MEDIA_ROOT = '/var/www/product/media/'
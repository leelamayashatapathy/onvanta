from .base import *  # noqa
from .base import DATABASE_URL
import dj_database_url

DEBUG = False

if not DATABASE_URL:
    raise RuntimeError('DATABASE_URL must be set in production.')

DATABASES = {
    'default': dj_database_url.parse(DATABASE_URL, conn_max_age=60),
}

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 60
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

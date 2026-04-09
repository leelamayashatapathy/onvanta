from .base import *  # noqa
from .base import env
import dj_database_url

DEBUG = True

ALLOWED_HOSTS = ['*']

# Local defaults: use localhost Postgres unless USE_DOCKER_DB=1
LOCAL_DATABASE_URL = env('DATABASE_URL', default='postgres://postgres:root@127.0.0.1:5432/onvanta')
if env('USE_DOCKER_DB', default=False):
    LOCAL_DATABASE_URL = 'postgres://postgres:root@db:5432/onvanta'

DATABASES = {
    'default': dj_database_url.parse(LOCAL_DATABASE_URL, conn_max_age=60),
}

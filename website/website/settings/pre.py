from .common import *

###################################################
# config env
###################################################
TEST_ENV = True
DEV_ENV = False
DEBUG = True

ALLOWED_HOSTS = ['*']

WSGI_APPLICATION = 'website.wsgi.pre.application'

DATABASES['default'] = {
    'ENGINE': 'django.db.backends.mysql',
    'NAME': 'doit',
    'USER': 'root',
    'PASSWORD': 'lipanpan@65',
    'HOST': '172.31.32.57',
    'PORT': '3306',
    'OPTIONS': {'charset': 'utf8mb4'},
}

REST_FRAMEWORK = {

    'DEFAULT_PERMISSION_CLASSES': ('framework.permission.UserRolePermission',),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ),
    'DEFAULT_PAGINATION_CLASS': 'framework.pagination.TablePageNumberPagination',
    'PAGE_SIZE': 10,
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'show_time': {
            'format': '%(asctime)s %(levelname)s [%(pathname)s %(funcName)s() line:%(lineno)s] [MSG]%(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'formatter': 'show_time',
            'class': 'logging.StreamHandler',
        }
    },
    'loggers': {
        'django.db.backends': {
            'handlers': ['console'],
            'propagate': False,
            'level': 'DEBUG',
        },
        'django.request': {
            'handlers': ['console'],
            'propagate': False,
            'level': 'DEBUG',
        }
    }
}

# 现象：可以正常的使用,可以正常的插入
# SESSION_COOKIE_AGE = 60 * 60 * 24
# CSRF_COOKIE_AGE = 60

# 可以正常的插入
# SESSION_COOKIE_AGE = 60
# CSRF_COOKIE_AGE = 60 * 60 * 24

# 设置过期时间为1天
SESSION_COOKIE_AGE = CSRF_COOKIE_AGE = 60 * 60 * 24
# SESSION_COOKIE_AGE = CSRF_COOKIE_AGE = 60


REDIS = {
    'host': 'localhost',
    'port': 6379,
    'db': 9,
}

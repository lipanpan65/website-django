# -*- coding: utf-8 -*-
# @Time    : 2022/6/13 5:37 下午
# @Author  : lipanpan65
# @Email  : 1299793997@qq.com
# @File  : prod.py
# @Desc :
from .common import *
from configparser import ConfigParser

DEBUG = False
ENV = "PROD"
TEST_ENV = False
DEV_ENV = False

LOG_PATH = '/var/log/website'

if not os.path.exists(LOG_PATH):
    os.mkdir(LOG_PATH)

###################################################
# config env
###################################################
ALLOWED_HOSTS = ["*"]
WSGI_APPLICATION = 'website.wsgi.prod.application'

db_config = ConfigParser()
db_config.read("/opt/conf/db.ini")

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.AllowAny',),  # 任何人
    # 'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.IsAuthenticated',),  # 必须通过认证
    # 'DEFAULT_PERMISSION_CLASSES': ('framework.permission.UserRolePermission',),
    # 从上向下执行走到如果校验成功则后面的不会校验
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        # 'rest_framework.renderers.JSONRenderer',
        'components.renderers.JSONRenderer',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ),
    'DEFAULT_PAGINATION_CLASS': 'components.pagination.SizeTablePageNumberPagination',
    # 'DEFAULT_PAGINATION_CLASS': 'components.pagination.TablePageNumberPagination',
    # 'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 5,
}

DATABASES['default'] = {
    'ENGINE': 'django.db.backends.mysql',
    'NAME': db_config.get('default', 'database'),
    'USER': db_config.get('default', 'user'),
    # 'PASSWORD': '%aKyWJ9nesb2',
    # 'PASSWORD': 'lipanpan#Web!wq10',
    'PASSWORD': db_config.get('default', 'password'),
    'HOST': db_config.get('default', 'host'),
    'PORT': '3306',
    'OPTIONS': {'charset': 'utf8mb4'},
}

###################################################
# redis config
###################################################

REDIS = {
    'host': 'localhost',
    'port': 6379,
    'db': 9,
}

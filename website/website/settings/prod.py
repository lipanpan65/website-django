# -*- coding: utf-8 -*-
# @Time    : 2022/6/13 5:37 下午
# @Author  : lipanpan65
# @Email  : 1299793997@qq.com
# @File  : prod.py
# @Desc :
from .common import *
from configparser import ConfigParser

DEBUG = False
TEST_ENV = False
DEV_ENV = False

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


###################################################
# 日志的配置
###################################################
LOG_PATH = '/var/log/website'
if not os.path.exists(LOG_PATH):
    os.mkdir(LOG_PATH)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        # 日志格式
        'standard': {
            'format': '[%(asctime)s] [%(filename)s:%(lineno)d] [%(module)s:%(funcName)s] '
                      '[%(levelname)s]- %(message)s'},
        'simple': {  # 简单格式
            'format': '[%(name)s] [%(levelname)s] %(message)s'
        },
        # 3[7mSuixinBlog: https://suixinblog.cn3[0m
        # \033[0;36m abc \033[0m
        'console': {
            'format': '[%(asctime)s] [%(name)s] [%(levelname)s] [%(filename)s:%(module)s:%(funcName)s:%(lineno)d] [%(processName)s:%(process)d] [%(threadName)s:%(thread)d] \033[1;36m %(message)s \033[0m'
        },
        # \033[0;37;42m\tHello World\033[0m
        # \033[0;37;40m
        # \033[0;36m
        # %(module)s %(funcName)s
        'db.backends': {
            'format': '\033[1;33m[%(name)s] [%(levelname)s] [%(processName)s:%(process)d] [%(threadName)s:%(thread)d]\n %(message)s \033[0m\n'
        },
    },
    # 过滤
    'filters': {
    },
    # 定义具体处理日志的方式
    'handlers': {
        # 默认记录所有日志
        'default': {
            'level': 'INFO',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(LOG_PATH, 'all-{}.log'.format(time.strftime('%Y-%m-%d'))),
            'when': 'midnight',
            'backupCount': 366,  # 备份数
            'formatter': 'standard',  # 输出格式
            'encoding': 'utf-8',  # 设置默认编码，否则打印出来汉字乱码
        },
        'django.request': {
            'level': 'INFO',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(LOG_PATH, 'django-request-{}.log'.format(time.strftime('%Y-%m-%d'))),
            'when': 'midnight',
            'backupCount': 366,  # 备份数
            'formatter': 'standard',  # 输出格式
            'encoding': 'utf-8',  # 设置默认编码
        },
        # 输出错误日志
        'error': {
            'level': 'ERROR',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(LOG_PATH, 'error-{}.log'.format(time.strftime('%Y-%m-%d'))),
            'when': 'midnight',
            'backupCount': 366,  # 备份数
            'formatter': 'standard',  # 输出格式
            'encoding': 'utf-8',  # 设置默认编码
        },
        # 控制台输出
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'console',  # 输出格式
        },
        'django.db.backends': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'db.backends',  # 输出格式
        },
        # 输出 access 日志 具体业务日志
        'access': {
            'level': 'INFO',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(LOG_PATH, 'access-{}.log'.format(time.strftime('%Y-%m-%d'))),
            'when': 'midnight',
            'backupCount': 366,  # 备份数
            'formatter': 'standard',  # 输出格式
            'encoding': 'utf-8',  # 设置默认编码
        },
    },
    # 配置用哪几种 handlers 来处理日志
    'loggers': {
        'django.request': {
            'handlers': ['django.request'],
            'level': 'INFO',  # 开发环境,测试环境都为 DEBUG
            'propagate': False
        },
        'django.db.backends': {
            'handlers': ['django.db.backends'],
            'propagate': False,
            'level': 'DEBUG',
        },
        # 类型 为 django 处理所有类型的日志， 默认调用 相当于 root
        'django': {
            # 'handlers': ['console', 'django.request'] if DEBUG else ['django.request'],
            'handlers': ['django.request'] if DEBUG else ['django.request'],
            'level': 'DEBUG' if DEBUG else 'INFO',
            'propagate': True
        },
        'error': {
            'handlers': ['console', 'error'] if DEBUG else ['error'],
            'level': 'DEBUG' if DEBUG else 'ERROR',
            'propagate': False
        },
        'access': {
            'handlers': ['console', 'access'] if DEBUG else ['access'],
            'level': 'DEBUG' if DEBUG else 'INFO',
            'propagate': False
        },
        'root': {
            'handlers': ['console', 'default'] if DEBUG else ['default'],
            'level': 'INFO'
        }
    }
}



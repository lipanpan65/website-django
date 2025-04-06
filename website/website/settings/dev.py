# -*- coding: utf-8 -*-
# @Time    : 2022/6/13 5:37 下午
# @Author  : lipanpan
# @Email  : 1299793997@qq.com
# @File  : dev.py
# @Desc :

from .common import *
from configparser import ConfigParser

db_config = ConfigParser()
db_config.read("/Users/lipanpan/github/website-django/website/website/settings/db.ini")

log_path = os.path.join(BASE_DIR, 'logs')

if not os.path.exists(log_path):
    os.mkdir(log_path)




# print(BASE_DIR)
###################################################
# config env
###################################################
DEBUG = True
ENV = "DEV"

TEST_ENV = True
DEV_ENV = True

ALLOWED_HOSTS = ['*']

DATABASES['default'] = {
    'ENGINE': 'django.db.backends.mysql',
    'NAME': db_config.get('default', 'database'),
    'USER': db_config.get('default', 'user'),
    'PASSWORD': db_config.get('default', 'password'),
    'HOST': db_config.get('default', 'host'),
    'PORT': db_config.get('default', 'port'),
    'OPTIONS': {'charset': 'utf8mb4'},
}

from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

REST_FRAMEWORK = {
    # 'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.AllowAny',),  # 任何人
    'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.IsAuthenticated',),  # 必须通过认证
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
    # 'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'EXCEPTION_HANDLER': 'components.exceptions.exception_handler',
    'DATETIME_FORMAT': "%Y-%m-%d %H:%M:%S",  # 例如：2022-04-07 15:30:00
    'DATE_FORMAT': "%Y-%m-%d",  # 例如：2022-04-07
}

# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'formatters': {
#         'show_time': {
#             'format': '%(asctime)s %(levelname)s [%(pathname)s %(funcName)s() line:%(lineno)s] [MSG]%(message)s',
#             'datefmt': '%Y-%m-%d %H:%M:%S',
#         }
#     },
#     'handlers': {
#         'console': {
#             'level': 'DEBUG',
#             'formatter': 'show_time',
#             'class': 'logging.StreamHandler',
#         }
#     },
#     'loggers': {
#         'django.db.backends': {
#             'handlers': ['console'],
#             'propagate': False,
#             'level': 'DEBUG',
#         },
#         'django.request': {
#             'handlers': ['console'],
#             'propagate': False,
#             'level': 'DEBUG',
#         }
#     }
# }

# # Cache to store session data if using the cache session backend.
# SESSION_CACHE_ALIAS = "default"
# # Cookie name. This can be whatever you want.
# SESSION_COOKIE_NAME = "sessionid"
# # Age of cookie, in seconds (default: 2 weeks).
# SESSION_COOKIE_AGE = 60 * 60 * 24 * 7 * 2
# # A string like "example.com", or None for standard domain cookie.
# SESSION_COOKIE_DOMAIN: Optional[str] = ...
# # Whether the session cookie should be secure (https:// only).
# SESSION_COOKIE_SECURE = False
# # The path of the session cookie.
# SESSION_COOKIE_PATH = "/"
# # Whether to use the non-RFC standard httpOnly flag (IE, FF3+, others)
# SESSION_COOKIE_HTTPONLY = True
# # Whether to set the flag restricting cookie leaks on cross-site requests.
# # This can be 'Lax', 'Strict', or None to disable the flag.
# SESSION_COOKIE_SAMESITE: Optional[str] = ...
# # Whether to save the session data on every request.
# SESSION_SAVE_EVERY_REQUEST = False
# # Whether a user's session cookie expires when the Web browser is closed.
# SESSION_EXPIRE_AT_BROWSER_CLOSE = False
# # The module to store session data
# SESSION_ENGINE = "django.contrib.sessions.backends.db"
# # Directory to store session files if using the file session module. If None,
# # the backend will use a sensible default.
# SESSION_FILE_PATH: Optional[str] = ...
# # class to serialize session data
# SESSION_SERIALIZER = "django.contrib.sessions.serializers.JSONSerializer"

# session 设置
# SESSION_COOKIE_NAME ＝ "sessionid"  # Session的cookie保存在浏览器上时的key，即：sessionid＝随机字符串（默认）
# SESSION_COOKIE_PATH ＝ "/"  # Session的cookie保存的路径（默认）
# SESSION_COOKIE_DOMAIN = None  # Session的cookie保存的域名（默认）
# SESSION_COOKIE_SECURE = False  # 是否Https传输cookie（默认）
# SESSION_COOKIE_HTTPONLY = True  # 是否Session的cookie只支持http传输（默认）
# SESSION_COOKIE_AGE = 60 * 60 * 24 * 7 * 2  # Session的cookie失效日期（2周）（数字为秒数）（默认）
# SESSION_COOKIE_AGE = 60 * 2  # Session的cookie失效日期（2周）（数字为秒数）（默认）
# SESSION_EXPIRE_AT_BROWSER_CLOSE = False  # 是否关闭浏览器使得Session过期（默认）
# SESSION_SAVE_EVERY_REQUEST = False  # 是否每次请求都保存Session，默认修改之后才保存（默认）

SESSION_COOKIE_AGE = 60 * 60 * 24 * 7 * 2

###################################################
# redis config
###################################################

REDIS = {
    'host': 'localhost',
    'port': 6379,
    'db': 9,
}

# -*- coding: utf-8 -*-
# @Time    : 2022/6/13 5:37 下午
# @Author  : lipanpan65
# @Email  : 1299793997@qq.com
# @File  : prod.py
# @Desc :
from .common import *

DEBUG = False
ENV = "PROD"
TEST_ENV = False
DEV_ENV = False

###################################################
# config env
###################################################
ALLOWED_HOSTS = ["*"]
WSGI_APPLICATION = 'website.wsgi.prod.application'
DATABASES['default'] = {
    'ENGINE': 'django.db.backends.mysql',
    'NAME': 'website',
    'USER': 'root',
    # 'PASSWORD': '%aKyWJ9nesb2',
    'PASSWORD': 'lipanpan#Web!wq10',
    'HOST': 'localhost',
    'PORT': '13380',
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

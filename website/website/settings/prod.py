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

###################################################
# config env
###################################################
ALLOWED_HOSTS = ["*"]
WSGI_APPLICATION = 'website.wsgi.prod.application'

db_config = ConfigParser()
db_ini = db_config.read("/opt/conf/db.ini")

default_database = db_ini["default"]

DATABASES['default'] = {
    'ENGINE': 'django.db.backends.mysql',
    'NAME': default_database['database'],
    'USER': default_database['user'],
    # 'PASSWORD': '%aKyWJ9nesb2',
    # 'PASSWORD': 'lipanpan#Web!wq10',
    'PASSWORD': default_database['password'],
    'HOST': default_database['host'],
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

"""
Django settings for website project.

Generated by 'django-admin startproject' using Django 4.2.8.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
import os
import time
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
# BASE_DIR = Path(__file__).resolve().parent.parent
# 新增 parent
BASE_DIR = Path(__file__).resolve().parent.parent.parent

log_path = os.path.join(BASE_DIR, 'logs')

if not os.path.exists(log_path):
    os.mkdir(log_path)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-n&d1dkr3p=5l+vwcy(8dj3x#rq!l-&ov)z!wzj)vv-hj5f+rq4'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'blog',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'website.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# WSGI_APPLICATION = 'website.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# 日志相关配置

LOG_PATH = os.path.join(BASE_DIR, 'logs')
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
            # 'formatter': 'standard' if DEBUG else 'standard',  # 输出格式
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

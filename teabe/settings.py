"""
Django settings for teabe project.

Generated by 'django-admin startproject' using Django 3.0.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
from decouple import config, Csv

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'letkz^iop=bj_c+41%7fm04hie$h_^xun=t(&k7ai207ad*0ea'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# bot token
TOKEN = config('TOKEN')
BOT_NAME = config('BOT_NAME')
HOLDER_ID = config('HOLDER_ID', cast=int)
BOT_CIPHER_CHANNEL = config('BOT_CIPHER_CHANNEL', cast=int)

# bot 前綴
PREFIX = config('PREFIX', cast=str)

# 成功反應
REACTION_SUCCESS = '🆗'

# 失敗反應
REACTION_FAILURE = '🆖'

# 向前反應
REACTION_FORWARD = '➡'

# 向後反應
REACTION_BACKWARD = '⬅'

REACTION_0 = '0️⃣'
REACTION_1 = '1️⃣'
REACTION_2 = '2️⃣'
REACTION_3 = '3️⃣'
REACTION_4 = '4️⃣'
REACTION_5 = '5️⃣'
REACTION_6 = '6️⃣'
REACTION_7 = '7️⃣'
REACTION_8 = '8️⃣'
REACTION_9 = '9️⃣'
REACTION_10 = '🔟'
REACTION_NEW = '🐇'
REACTION_ADMIN = '🔓'

# CELERY 設定
# CELERY_BROKER_URL = 'redis://localhost:6379' # 不設定也能運作
# CELERY_BACKEND_URL = 'redis://localhost:6379' # 不設定也能運作

CELERY_RESULT_BACKEND = 'django-db'
CELERY_CACHE_BACKEND = 'default'

# logging
MAIN_LOG_PATH = os.path.join(BASE_DIR, 'logs/main.log')
LOG_DIR = os.path.dirname(MAIN_LOG_PATH)
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

LOGGING_CONFIG = 'logging.config.dictConfig'
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s %(levelname)s %(name)s %(module)s: %(message)s'
        }

    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
        },
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': MAIN_LOG_PATH,
            'maxBytes': 1024*1024*10,
            'backupCount': 10,
            'formatter': 'standard',
        }
    },
    'loggers': {
        'bot': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
    'filters': {}
}

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'bot.apps.BotConfig',
    'django_celery_beat',
    'django_celery_results',
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

ROOT_URLCONF = 'teabe.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'bot')],
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

WSGI_APPLICATION = 'teabe.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'zh-hant'

TIME_ZONE = 'Asia/Taipei'

USE_I18N = True

USE_L10N = True

USE_TZ = True

CELERY_TIMEZONE = TIME_ZONE

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'

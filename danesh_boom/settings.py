"""
Django settings for danesh_boom project.

Generated by 'django-admin startproject' using Django 1.10.5.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os
from danesh_boom.settings_helpers import get_config, get_db_settings, load_static_asset_manifest
from django.utils.translation import ugettext_lazy as _
import datetime

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
from danesh_boom.social_auth_pipeline import LOCAL_SOCIAL_AUTH_PIPELINE

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CONFIG = get_config(BASE_DIR)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = CONFIG.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = CONFIG.get('DEBUG')

ALLOWED_HOSTS = CONFIG.get('ALLOWED_HOSTS')

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'social_django',
    'graphene_django',
    'base',
    'users',
    'organizations',
    'media',
    'products',
    'chats',
    'exchanges',
    'forms',
    'rest_framework',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware',
]

JWT_AUTH = {
    'JWT_ENCODE_HANDLER':
    'rest_framework_jwt.utils.jwt_encode_handler',

    'JWT_DECODE_HANDLER':
    'rest_framework_jwt.utils.jwt_decode_handler',

    'JWT_PAYLOAD_HANDLER':
    'rest_framework_jwt.utils.jwt_payload_handler',

    'JWT_PAYLOAD_GET_USER_ID_HANDLER':
    'rest_framework_jwt.utils.jwt_get_user_id_from_payload_handler',

    'JWT_RESPONSE_PAYLOAD_HANDLER':
    'rest_framework_jwt.utils.jwt_response_payload_handler',

    'JWT_SECRET_KEY': SECRET_KEY,
    'JWT_GET_USER_SECRET_KEY': None,
    'JWT_PUBLIC_KEY': None,
    'JWT_PRIVATE_KEY': None,
    'JWT_ALGORITHM': 'HS256',
    'JWT_VERIFY': True,
    'JWT_VERIFY_EXPIRATION': True,
    'JWT_LEEWAY': 0,
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=15),
    'JWT_AUDIENCE': None,
    'JWT_ISSUER': None,

    'JWT_ALLOW_REFRESH': False,
    'JWT_REFRESH_EXPIRATION_DELTA': datetime.timedelta(days=7),

    'JWT_AUTH_HEADER_PREFIX': 'JWT',
    'JWT_AUTH_COOKIE': None,

}

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
}

ROOT_URLCONF = 'danesh_boom.urls'

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
                'users.context_processors.static',
            ],
        },
    },
]

AUTHENTICATION_BACKENDS = (
    'social_core.backends.google.GoogleOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)

WSGI_APPLICATION = 'danesh_boom.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': get_db_settings(CONFIG)
}

# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

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

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}

CACHE_TIMEOUT = 60 * 60 * 24 

# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

LANGUAGE_SESSION_KEY = 'LANG'
LANGUAGES = [
    ('fa', _('Persian')),
    ('en', _('English')),
]
LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale'),
]
TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

if CONFIG.get('EMAIL').get('ENABLE_SMTP'):
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = CONFIG.get('EMAIL').get('HOST')
EMAIL_HOST_USER = CONFIG.get('EMAIL').get('HOST_USER')
EMAIL_HOST_PASSWORD = CONFIG.get('EMAIL').get('HOST_PASSWORD')
EMAIL_PORT = CONFIG.get('EMAIL').get('PORT')
EMAIL_USE_TLS = CONFIG.get('EMAIL').get('USE_TLS')
EMAIL_FROM = CONFIG.get('EMAIL').get('EMAIL_FROM')

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'

FRONTEND_DEV = CONFIG.get('FRONTEND_DEV')
FRONTEND_ROOT = os.path.join(BASE_DIR, CONFIG.get('FRONTEND_ROOT'))
FRONTEND_BUILD_ROOT = os.path.join(
    FRONTEND_ROOT, CONFIG.get('FRONTEND_BUILD_ROOT'))

STATICFILES_DIRS = [
    #os.path.join(BASE_DIR, 'static'),
]
#STATIC_ROOT = os.path.join(BASE_DIR, CONFIG.get('STATIC_ROOT'))

STATIC_ASSET_MANIFEST = load_static_asset_manifest(
    FRONTEND_BUILD_ROOT, FRONTEND_DEV)

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = CONFIG.get('SOCIAL_AUTH_GOOGLE_OAUTH2_KEY')
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = CONFIG.get(
    'SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET')
SOCIAL_AUTH_PIPELINE = LOCAL_SOCIAL_AUTH_PIPELINE
SOCIAL_AUTH_RAISE_EXCEPTIONS = False

# TODO improve visible urls
SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/#/auth/logged-in/'
SOCIAL_AUTH_LOGIN_ERROR_URL = '/#/auth/login-error/'
SOCIAL_AUTH_LOGIN_URL = '/#/auth/login/'
SOCIAL_AUTH_NEW_ASSOCIATION_REDIRECT_URL = '/#/auth/new-association/'
SOCIAL_AUTH_DISCONNECT_REDIRECT_URL = '/#/auth/account-disconnected/'
SOCIAL_AUTH_INACTIVE_USER_URL = '/#/auth/inactive-user/'

GRAPHENE = {
    'SCHEMA': 'danesh_boom.schema.schema',
    'SCHEMA_OUTPUT': os.path.join(
        BASE_DIR,
        FRONTEND_ROOT,
        'graphql.schema.json'),
}

# x-sendfile
SENDFILE_BACKEND = CONFIG.get('SENDFILE_BACKEND')
SENDFILE_ROOT = os.path.normpath(
    os.path.join(
        BASE_DIR,
        CONFIG.get('SENDFILE_ROOT')))
SENDFILE_URL = CONFIG.get('SENDFILE_URL')
# not MEDIA_ROOT. this is media app settings
MEDIA_DIR = os.path.join(SENDFILE_ROOT, 'media')

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

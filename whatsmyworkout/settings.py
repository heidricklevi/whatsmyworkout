"""
Django settings for whatsmyworkout project.

Generated by 'django-admin startproject' using Django 1.10.4.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os
import whatsmyworkout.config
import datetime
# from custom_storages import StaticStorage


CONFIG_ALLOW_HOSTS = whatsmyworkout.config.CONFIG_ALLOW_HOSTS
email_config = whatsmyworkout.config.email_config
database_config = whatsmyworkout.config.database_config
AWS_CONFIG = whatsmyworkout.config.AWS_CONFIG


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '$d9y415c(s)q%-5^*8d3y^x*x(902t_ui-86k*33g-)kb%imqi'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = CONFIG_ALLOW_HOSTS

# Email settings
EMAIL_HOST = email_config['EMAIL_HOST']
EMAIL_HOST_PASSWORD = email_config['EMAIL_HOST_PASSWORD']
EMAIL_HOST_USER = email_config['EMAIL_HOST_USER']
EMAIL_PORT = email_config["EMAIL_PORT"]
EMAIL_USE_TLS = email_config["EMAIL_USE_TLS"]
DEFAULT_FROM_EMAIL = email_config["DEFAULT_FROM_EMAIL"]
SERVER_EMAIL = email_config["SERVER_EMAIL"]

LOGIN_REDIRECT_URL = '/'

REST_FRAMEWORK = {

    'PAGE_SIZE': 25,
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],

    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),

    'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend',),

}

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'account',
    'widget_tweaks',
    'rest_framework.authtoken',
    'rest_framework',
    'anymail',
    'rest_auth',
    'corsheaders',
    'reversion',
    'storages',
    'friendship',
    'django_filters',
    'django_celery_results',
]

# EMAIL_BACKEND = "anymail.backends.mailgun.EmailBackend"

ANYMAIL = {
    # (exact settings here depend on your ESP...)
    "MAILGUN_API_KEY": email_config['MAIL_GUN_API_KEY'],
    "MAILGUN_SENDER_DOMAIN": email_config['MAIL_GUN_SENDER_DOMAIN'],  # your Mailgun domain, if needed
}


CORS_ORIGIN_ALLOW_ALL = True
REST_USE_JWT = True

JWT_AUTH = {
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=7),
    'JWT_RESPONSE_PAYLOAD_HANDLER': 'account.helper.jwt_response_payload_handler',
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'reversion.middleware.RevisionMiddleware',

    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CORS_ALLOW_CREDENTIALS = True
CSRF_TRUSTED_ORIGINS = (
    '127.0.0.1:8000',
    '127.0.0.1:8081',
)

CORS_ORIGIN_WHITELIST = (
    'http://127.0.0.1:8081',
    'localhost:8081/',
    'http://127.0.0.1:8081/',
    'https://services.whatsmyworkout.co',
    'services.whatsmyworkout.co',
    'https://www.whatsmyworkout.co',
    'www.whatsmyworkout.co',
)

CORS_ALLOW_HEADERS = (
    'x-requested-with',
    'content-type',
    'accept',
    'origin',
    'Authorization',
    'X-CSRFToken',
)

ROOT_URLCONF = 'whatsmyworkout.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'whatsmyworkout/../../../account/../../account/templates')]
        ,
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

WSGI_APPLICATION = 'whatsmyworkout.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': database_config['NAME'],
        'USER': database_config['USER'],
        'PASSWORD': database_config['PASSWORD'],
        'HOST': database_config['HOST'],
        'PORT': database_config['PORT']
    }
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


# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

AWS_STORAGE_BUCKET_NAME = AWS_CONFIG['AWS_STORAGE_BUCKET_NAME']
AWS_ACCESS_KEY_ID = AWS_CONFIG['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = AWS_CONFIG['AWS_SECRET_ACCESS_KEY']
#
STATICFILES_LOCATION = 'static'
STATICFILES_STORAGE = 'whatsmyworkout.custom_storages.StaticStorage'
# STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

MEDIAFILES_LOCATION = 'media'
DEFAULT_FILE_STORAGE = 'whatsmyworkout.custom_storages.MediaStorage'


# Tell django-storages the domain to use to refer to static files.
AWS_S3_CUSTOM_DOMAIN = 's3.amazonaws.com/%s' % AWS_STORAGE_BUCKET_NAME

# Tell the staticfiles app to use S3Boto3 storage when writing the collected static files (when
# you run `collectstatic`).

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/
STATIC_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, STATICFILES_LOCATION)
# STATIC_URL = '/static/'
#
STATIC_ROOT = os.path.join(BASE_DIR, '../../account/../../account/static/')
#
#
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# CELERY CONFIGURATION

CELERY_RESULT_BACKEND = 'django-db'
CELERY_BROKER_URL = 'amqp://localhost'


# Custom Command Logging config (send emails)


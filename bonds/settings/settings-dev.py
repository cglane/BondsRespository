"""
Django settings for bonds project.

Generated by 'django-admin startproject' using Django 1.11.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
import sys
from dotenv import load_dotenv, find_dotenv
load_dotenv()

def location(x):
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), x)

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'mxvt5@g-&cszmt91m(u7+_%l&yd_i8psx*f*e8d0a))%wd3t-#'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

LOGIN_HEADER = "Shelmore Surety"

POWERS_EXPIRATION = 90

POWERS_EXPIRATION_TRANSFER = 30

BOND_PREMIUM = .00781

AUTH_USER_MODEL = 'powers.User'

BOND_PRINT_CONTENT_ONE = 'KNOW ALL MEN BY THESE PRESENTS: that {0}, a corporation duly authorized and existing under the laws of the State of South Carolina does constitute and appoint the below named agent its true and lawful Attorney-In-Fact for it and in its name, place and stead, to execute, and deliver for and on its behalf, as surety, a bail bond only.'

BOND_PRINT_CONTENT_TWO = 'Authority of such a Attorney-In-Fact is limited to appearance bonds. No authority is provided herein for the execution of surety immigration bonds or to guarantee alimony payments, fines, wage law claims or other payments of any kind on behalf of below named defendant. The named agent is appointed only to execute the bond consistent with the terms of this power of attorney. The agents is not authorized to act as agent for receipt of service of process in any criminal or civil action. This power is void if altered or erased or used in any combination with other powers of attorney of the company or any other company to obtain the release of the defendant named below or to satisfy any bond requirement in excess of the stated face amount of this power. This power can only be used once. The obligation of the company shall not exceed the sum of'

BOND_PRINT_CONTENT_THREE = 'and provided this Power-Of-Attorney is filed with the bond and retained as a part of the court records. The said Attorney-In-Fact is hereby authorized to insert in this Power-Of-Attorney the name of the person on whose behalf this bond was given.'

BOND_PRINT_CONTENT_FOUR = "IN WITNESS WHEREOF, {0} has caused these presents to be signed by it's duly authorized officer, proper for the purpose and its corporate seal to be herunto affixed this <span class='long-date'>{1}</span>."
# Application definition

VOID_WHITELIST = ['charleslane23@gmail.com',
                  'mfarmer@thefarmerlawfirm.com',
                  'lowndes.sinkler@sinklerbonding.com',
                  'hward@shelmoresurety.com',
                  'lshirley@shelmoresurety.com',
                  ]

POWERS_TYPES = (('5000.00', '5000.00'), ('15000.00', '15000.00'),
                ('25000.00', '25000.00'), ('50000.00', '50000.00'), ('99000.00', '99000.00'),
                ('100000.00', '100000.00'), ('150000.00', '150000.00'),
                ('250000.00', '250000.00'), ('500000.00', '500000.00'))

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
ADMIN_EMAILS = ['lshirley@shelmoresurety.com']
EMAIL_HOST_USER = os.environ['BONDS_EMAIL_ADDRESS']
EMAIL_HOST_PASSWORD = os.environ['BONDS_EMAIL_PASSWORD']

INSTALLED_APPS = [
    'jet', 'django.contrib.auth',
    'django.contrib.contenttypes', 'django.contrib.sessions',
    'django.contrib.messages', 'django.contrib.staticfiles',
    'powers.apps.AppConfig', 'powers.apps.CustomAdminConfig',
    'storages','report_builder', 'django_admin_listfilter_dropdown',

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

ROOT_URLCONF = 'bonds.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, '..', 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.static',
                'django.template.context_processors.media'
            ],
        },
    },
]
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
    )
}
WSGI_APPLICATION = 'bonds.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

if os.environ.get('ENVIRONMENT_NAME') == 'development':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': os.environ['RDS_DB_NAME'],
            'USER': os.environ['RDS_USERNAME'],
            'PASSWORD': os.environ['RDS_PASSWORD'],
            'HOST': os.environ['RDS_HOSTNAME'],
            'PORT': os.environ['RDS_PORT'],
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'ebdb',
            'USER': 'postgres',
            'PASSWORD': os.environ.get('BOND_DEV_PASSWORD'),
            'HOST': os.environ.get('BOND_DEV_HOST'),
            'PORT': '5432',
        }
    }

if 'test' in sys.argv:
    print('sys')
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),

        }
    }

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME':
        'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'US/Eastern'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

# STATIC_ROOT = location('public/static')
# STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "..", "static"),
)


AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID_BONDS')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY_BONDS')

AWS_STORAGE_BUCKET_NAME = 'static-bonds'
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}
AWS_LOCATION = 'static'

MEDIAFILES_LOCATION = 'media'
MEDIA_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, MEDIAFILES_LOCATION)


STATIC_URL = 'https://%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION)

STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

print('made it here')
#


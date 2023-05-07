"""
Django settings for career_proj project.

Generated by 'django-admin startproject' using Django 4.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""
import json
from datetime import timedelta
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-x&h4=c7n!25d1cl17^bhi31!xd&)byf1f91_wp+g8wuz6rafw4'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
ALLOWED_HOSTS = ['127.0.0.1', 'localhost']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django_crontab',

    'django_countries',
    'djmoney',

    'corsheaders',
    'rest_framework',
    'rest_framework_simplejwt',
    'django_filters',

    'jobs_app.apps.JobsAppConfig'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',

    'corsheaders.middleware.CorsMiddleware', # !!!

    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',


]

ROOT_URLCONF = 'career_proj.urls'

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

WSGI_APPLICATION = 'career_proj.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases


# Getting user & password for DATABASE
# career_db_key_link = "/Users/victoraynbinder/Documents/keys/career_db_key.json"

career_db_key_link = "/home/ubuntu/src/keys/career_db_key.json"

with open(career_db_key_link, 'r') as fh:
    credentials = json.load(fh)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'career',
        'USER': str(credentials['USER']),
        'PASSWORD': str(credentials['PASSWORD']),
        'HOST': 'localhost',
        'PORT': '5432',
    }
}



# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field




DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CORS_ALLOW_ALL_ORIGINS = True

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10
}

SIMPLE_JWT = {
    # "ACCESS_TOKEN_LIFETIME": timedelta(minutes=1),
    # "REFRESH_TOKEN_LIFETIME": timedelta(minutes=45)

    "ACCESS_TOKEN_LIFETIME": timedelta(days=5),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=10)
}

# Countries settings
COUNTRIES_FIRST = [ 'US', 'IL' ]

# CRONJOBS = [
#     # ('* * * * *', 'myapp.cron.my_scheduled_job')
#     # ('* * * * *', 'jobs_app.run_scraper.run_linkedin_scrap_process')
# ('* * * * *', 'jobs_app.run_scraper.run_linkedin_scrap_process','>> /tmp/linkedin_scraper.log 2>&1')
# ]

CRONJOBS = [
    # ('* * * * *', 'myapp.cron.my_scheduled_job')
    # ('* * * * *', 'jobs_app.run_scraper.run_linkedin_scrap_process')
('* * * * *', 'jobs_app.run_scraper.run_linkedin_scrap_process','>> /tmp/linkedin_scraper.log 2>&1')
]

# CRONJOBS = [
#     # ('* * * * *', 'myapp.cron.my_scheduled_job')
#     # ('* * * * *', 'jobs_app.run_scraper.run_linkedin_scrap_process')
# ('* * * * *','DJANGO_SETTINGS_MODULE=career_proj.prod_settings',  'jobs_scrappers.linkedin_scrapper.get_linkedin_jobs_to_db.py','>> /tmp/linkedin_scraper.log 2>&1')
# ]
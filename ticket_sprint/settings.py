"""
Django settings for TicketSprint project.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()  # Load the config file.

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-ydl6zt7_l9wro$d94nouo3eifnlzw9h-)3gt+uue+d$k8#glc='

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
    'ticketing.apps.TicketingConfig',
    'venue_management.apps.VenueManagementConfig'
]
#AUTH_USER_MODEL = 'ticketing.Eventgoer'
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'ticketing.backends.EventgoerBackend',
    'venue_management.backends.VenueManagerBackend'
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

ROOT_URLCONF = 'ticket_sprint.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
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

WSGI_APPLICATION = 'ticket_sprint.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
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

LANGUAGE_CODE = 'en-ca'

TIME_ZONE = 'America/Toronto'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/
STATIC_URL = 'static/'
STATICFILES_DIRS = [
    BASE_DIR / "static",
]
# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Email Settings (SMTP)
# https://docs.djangoproject.com/en/4.1/topics/email/#smtp-backend
try:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = os.getenv('SMTP_HOST')
    EMAIL_PORT = int(os.getenv('SMTP_PORT'))
    EMAIL_HOST_USER = os.getenv('SMTP_HOST_USER')
    EMAIL_HOST_PASSWORD = os.getenv('SMTP_HOST_PASSWORD')
    EMAIL_USE_SSL = os.getenv('SMTP_USE_SSL').lower() == 'true'
    EMAIL_USE_TLS = os.getenv('SMTP_USE_TLS').lower() == 'true'
    EMAIL_SUBJECT_PREFIX = os.getenv('EMAIL_SUBJECT_PREFIX').strip("'")
    DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL')
    EMAIL_SSL_KEYFILE = None if os.getenv('EMAIL_SSL_KEYFILE').lower() == 'none' else os.getenv('EMAIL_SSL_KEYFILE')
    EMAIL_SSL_CERTFILE = None if os.getenv('EMAIL_SSL_CERTFILE').lower() == 'none' else os.getenv('EMAIL_SSL_CERTFILE')
    EMAIL_TIMEOUT = None if os.getenv('EMAIL_TIMEOUT').lower() == 'none' else int(os.getenv('EMAIL_TIMEOUT'))
except TypeError:
    print(".env file missing. Email support disabled.")

# Caching Backend
# https://docs.djangoproject.com/en/dev/topics/cache/
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'django_cache',
    }
}

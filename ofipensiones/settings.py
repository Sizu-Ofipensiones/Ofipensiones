"""
Django settings for ofipensiones project.

Generated by 'django-admin startproject' using Django 5.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-^92_+d_hx#r09ti1l*ky7_b!z&t__ya_gjwziyglck&j#+egss'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'social_django',
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

ROOT_URLCONF = 'ofipensiones.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'ofipensiones', 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends',  # Requerido para Auth0
                'social_django.context_processors.login_redirect',  # Requerido para Auth0
            ],
        },
    },
]

WSGI_APPLICATION = 'ofipensiones.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases





# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = '/static/'


# Configuración de Auth0
LOGIN_URL = "/login/auth0"
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "https://dev-pnpogkrkp7l1bdda.us.auth0.com/v2/logout?returnTo=http%3A%2F%2F34.27.107.190:8080"

SOCIAL_AUTH_TRAILING_SLASH = False  # Elimina la barra final en rutas
SOCIAL_AUTH_AUTH0_DOMAIN = 'dev-pnpogkrkp7l1bdda.us.auth0.com'
SOCIAL_AUTH_AUTH0_KEY = 'OdEYKwyKqdb4ejOqhhxSBBzYxWS3ybt1'
SOCIAL_AUTH_AUTH0_SECRET = 'ENi9bP0uyZSqdpvcn_V42zuojnCYew2K6XT8cfE9cYom-1qI1T7NkpPyyeuuNmd5'

SOCIAL_AUTH_AUTH0_SCOPE = [
    'openid',  # Identificación del usuario
    'profile', # Información básica
    'email',   # Dirección de correo
    'role',    # Roles personalizados (si los configuras en Auth0)
]

AUTHENTICATION_BACKENDS = (
    'ofipensiones.auth0Backend.Auth0',  # Backend de Auth0
    'django.contrib.auth.backends.ModelBackend',  # Backend de Django
)

"""
Django settings for ofipensiones project.

Generated by 'django-admin startproject' using Django 5.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-^92_+d_hx#r09ti1l*ky7_b!z&t__ya_gjwziyglck&j#+egss'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [*]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Aplicaciones propias
    'users',
    'payments',
    'messageBus',
    'reports',
    # Integración con Auth0
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
        'DIRS': [],
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

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'db_users',  
        'USER': 'postgres',    
        'PASSWORD': '12345',  
        'HOST': '10.128.0.5',   
        'PORT': '5432',        
    }
}



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

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Configuración de Auth0
LOGIN_URL = "/login/auth0"
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = (
    "https://your-auth0-domain.auth0.com/v2/logout"
    "?returnTo=http%3A%2F%2Fyour-app-url:8000"
)

SOCIAL_AUTH_TRAILING_SLASH = False  # Elimina la barra final en rutas
SOCIAL_AUTH_AUTH0_DOMAIN = 'your-auth0-domain.auth0.com'
SOCIAL_AUTH_AUTH0_KEY = 'your-client-id'
SOCIAL_AUTH_AUTH0_SECRET = 'your-client-secret'

SOCIAL_AUTH_AUTH0_SCOPE = [
    'openid',  # Identificación del usuario
    'profile', # Información básica
    'email',   # Dirección de correo
    'role',    # Roles personalizados (si los configuras en Auth0)
]

AUTHENTICATION_BACKENDS = (
    'social_core.backends.auth0.Auth0OAuth2',  # Backend de Auth0
    'django.contrib.auth.backends.ModelBackend',  # Backend de Django
)

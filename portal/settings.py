"""
Django settings for portal project.

Generated by 'django-admin startproject' using Django 3.2.6.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'sealed_secret')

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
    'mozilla_django_oidc',
    'portal'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'mozilla_django_oidc.middleware.SessionRefresh',
    'portal.middleware.TokenCookieMiddleWare'
]

ROOT_URLCONF = 'portal.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'portal.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTHENTICATION_BACKENDS = (
    'portal.middleware.OIDCAB',

)
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

OIDC_RP_CLIENT_ID = os.environ.get("OIDC_RP_CLIENT_ID", 'client_id')
OIDC_RP_CLIENT_SECRET = os.environ.get("OIDC_RP_CLIENT_SECRET",'client_secret')
OIDC_OP_AUTHORIZATION_ENDPOINT = os.environ.get("OIDC_OP_AUTHORIZATION_ENDPOINT","https://aai.coih.org/oxauth/restv1/authorize")
OIDC_OP_TOKEN_ENDPOINT = os.environ.get("OIDC_OP_TOKEN_ENDPOINT","https://aai.coih.org/oxauth/restv1/token")
OIDC_OP_USER_ENDPOINT = os.environ.get("OIDC_OP_USER_ENDPOINT","https://aai.coih.org/oxauth/restv1/userinfo")
#OIDC_TOKEN_USE_BASIC_AUTH = os.environ.get("OIDC_TOKEN_USE_BASIC_AUTH", True)
OIDC_RP_SIGN_ALGO = os.environ.get('OIDC_RP_SIGN_ALGO','RS256')
OIDC_OP_JWKS_ENDPOINT = os.environ.get("OIDC_OP_JWKS_ENDPOINT","https://aai.coih.org/oxauth/restv1/jwks")
OIDC_USE_NONCE = False
#OIDC_CREATE_USER = False
OIDC_STORE_ACCESS_TOKEN = True
OIDC_STORE_ID_TOKEN = True

TOKEN_ID_COOKIE = os.environ.get('TOKEN_ID_COOKIE',"auth_user_id")
OIDC_RP_SCOPES = "openid user_name is_operator"


USER_PREFIX = os.environ.get('USER_PREFIX','user-prefix')
HOSTNAME = os.environ.get('HOSTNAME','localhost')
SESSION_COOKIE_DOMAIN = '.' + str(HOSTNAME)
AUTHHOST = os.environ.get('AUTHHOST','auth')
PORTALHOST = os.environ.get('PORTALHOST','portal')
# OIDC_VERIFY_SSL - assume True unless False is explicitly specified
OIDC_VERIFY_SSL = not os.environ.get("OIDC_VERIFY_SSL", "True").lower() in ("false", "0", "f")

def provider_logout(request):

    redirect_url = 'https://'+ str(AUTHHOST)+ '.' + str(HOSTNAME) + '/oxauth/restv1/end_session?post_logout_redirect_uri=https://'+ str(PORTALHOST)+ '.' + str(HOSTNAME)
    return redirect_url

OIDC_OP_LOGOUT_URL_METHOD='portal.settings.provider_logout'
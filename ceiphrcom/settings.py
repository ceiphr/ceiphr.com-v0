import os
import ceiphrcom.production_config
import sentry_sdk
from csp import context_processors
from sentry_sdk.integrations.django import DjangoIntegration

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!

SECRET_KEY = ceiphrcom.production_config.secret_key

# SECURITY WARNING: don't run with debug turned on in production!

DEBUG = ceiphrcom.production_config.debug

ADMIN_ENABLED = True

APPEND_SLASH = True

ALLOWED_HOSTS = ['ceiphr.com', '127.0.0.1',
                 'localhost', '0.0.0.0', '142.93.177.255']

OTP_TOTP_ISSUER = 'Ceiphr'

HTML_MINIFY = True

# Content Security Policy

CSP_INCLUDE_NONCE_IN=['script-src']

CSP_IMG_SRC = ("'self'", 'https://*.ceiphr.com', 'https://i.creativecommons.org',
               'https://licensebuttons.net', 'https://*.buysellads.net', 'https://ad.doubleclick.net')

CSP_STYLE_SRC = ("'self' 'unsafe-inline'")

CSP_SCRIPT_SRC = ("'self' 'sha256-fjjpQlVVyxtf9t0sPF+ZsZwcAHJ013VPXtsLT6LGavQ='", 'https://*.ceiphr.com', 'https://*.carbonads.com',
                  'https://cdnjs.cloudflare.com', 'https://*.google.com', 'https://*.gstatic.com', 'https://google.com', 
                  'https://gstatic.com', 'https://*.carbonads.net')

CSP_FONT_SRC = ("'self' data:", 'https://cdnjs.cloudflare.com')

CSP_FRAME_SRC = ("'self'", 'https://*.google.com', 'https://*.gstatic.com')

CSP_CONNECT_SRC = ("'self'", )

CSP_OBJECT_SRC = ("'none'", )

CSP_BASE_URI = ("'none'", )

CSP_FRAME_ANCESTORS = ("'none'", )

CSP_FORM_ACTION = ("'self'")

# Application definition

INSTALLED_APPS = [
    'jet.dashboard',
    'jet',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    'database',
    'snowpenguin.django.recaptcha2',
    'pipeline',
    'sorl.thumbnail',
    'django_otp',
    'django_otp.plugins.otp_totp',
    'django_otp.plugins.otp_hotp',
    'django_otp.plugins.otp_static',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'csp.middleware.CSPMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django_otp.middleware.OTPMiddleware',
    'htmlmin.middleware.HtmlMinifyMiddleware',
    'htmlmin.middleware.MarkRequestMiddleware',
    # 'django.middleware.gzip.GZipMiddleware',
    # 'pipeline.middleware.MinifyHTMLMiddleware',
]

ROOT_URLCONF = 'ceiphrcom.urls'

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

WSGI_APPLICATION = 'ceiphrcom.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases
if DEBUG:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'ceiphrcom',
            'USER': 'ceiphrcom',
            'PASSWORD': ceiphrcom.production_config.postgres_PW,
            'HOST': 'localhost',
            'PORT': '',
        }
    }


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/New_York'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'pipeline.finders.PipelineFinder',
)

PIPELINE = {
    # Convert Sass files to four minimized CSS files
    'STYLESHEETS': {
        'critical': {
            'source_filenames': (
                'sass/index.scss',
                'sass/rain.scss',
            ),
            'output_filename':
            'css/index.css',
            'extra_context': {
                'preload': False,
            },
        },
        'article': {
            'source_filenames': (
                'sass/article.scss',
                'sass/monokai.scss',
            ),
            'output_filename':
            'css/article.css',
            'extra_context': {
                'preload': False,
            },
        },
        'fonts': {
            'source_filenames': (
                'node_modules/@ibm/plex/css/ibm-plex.css',
            ),
            'output_filename':
            'css/fonts.css',
            'extra_context': {
                'preload': False,
            },
        },       
        'frameworks': {
            'source_filenames': (
                'node_modules/materialize-css/sass/materialize.scss',
            ),
            'output_filename':
            'css/frameworks.css',
        },
    },

    # Minimize and condense javascript into two files
    'JAVASCRIPT': {
        'onload': {
            'source_filenames': (
                'node_modules/lazysizes/lazysizes.js',
                'node_modules/fg-loadcss/dist/cssrelpreload.min.js',
            ),
            'output_filename':
            'js/onload.js',
            'extra_context': {
                'async': True,
            },
        },
        'frameworks': {
            'source_filenames': (
                'node_modules/jquery/dist/jquery.min.js',
                'node_modules/materialize-css/dist/js/materialize.min.js',
                'js/base.js',
            ),
            'output_filename':
            'js/frameworks.js',
            'extra_context': {
                'defer': True,
            },
        }
    }
}

PIPELINE['COMPILERS'] = (
    'pipeline.compilers.sass.SASSCompiler',
)

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

STATICFILES_DIRS = (os.path.join(BASE_DIR, 'assets'),)

STATIC_URL = '/static/'

# Media files

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

MEDIA_URL = '/media/'

# Production debugging via sentry.io
if not DEBUG:
    sentry_sdk.init(
        dsn=ceiphrcom.production_config.sentry_dsn ,
        integrations=[DjangoIntegration()]
    )

# Email System

if not DEBUG:
    EMAIL_BACKEND = "sendgrid_backend.SendgridBackend"

    SENDGRID_API_KEY = ceiphrcom.production_config.sendgrid_key

else:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

    DEFAULT_FROM_EMAIL = 'testing@example.com'

    EMAIL_HOST_USER = ''

    EMAIL_HOST_PASSWORD = ''

    EMAIL_USE_TLS = False

    EMAIL_PORT = 1025

# Security for production server use.
# See https://docs.djangoproject.com/en/2.0/ref/middleware/#module-django.middleware.security for details.

if not DEBUG:
    SECURE_SSL_REDIRECT = True

    SESSION_COOKIE_SECURE = True

    CSRF_COOKIE_SECURE = True

    SECURE_CONTENT_TYPE_NOSNIFF = True

    SECURE_BROWSER_XSS_FILTER = True

    SECURE_HSTS_SECONDS = 31536000

    SECURE_HSTS_PRELOAD = True

    SECURE_HSTS_INCLUDE_SUBDOMAINS = True

    X_FRAME_OPTIONS = 'DENY'

# ReCaptcha System

if not DEBUG:
    RECAPTCHA_PUBLIC_KEY = ceiphrcom.production_config.recap_sitekey

    RECAPTCHA_PRIVATE_KEY = ceiphrcom.production_config.recap_privkey

else:
    RECAPTCHA_PUBLIC_KEY = ""

    RECAPTCHA_PRIVATE_KEY = ""

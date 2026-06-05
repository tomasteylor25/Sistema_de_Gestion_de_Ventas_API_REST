"""
Django settings - Sistema de Gestión de Ventas
"""

import os
from pathlib import Path
from datetime import timedelta

import environ

# ─── Paths ───────────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent

# ─── Environ ─────────────────────────────────────────────────────────────────
env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# ─── Seguridad ───────────────────────────────────────────────────────────────
SECRET_KEY = env('SECRET_KEY', default='django-insecure-cambiar-en-produccion')
DEBUG = env.bool('DEBUG', default=True)
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['localhost', '127.0.0.1'])

# ─── Apps instaladas ─────────────────────────────────────────────────────────
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Terceros
    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'django_filters',
    'drf_spectacular',
    # Apps propias
    'api.autenticacion',
    'api.clientes',
    'api.productos',
    'api.proveedores',
    'api.sucursales',
    'api.pedidos',
    'api.detalle_pedidos',
    'api.facturas',
    'api.pagos',
]

# ─── Middleware ───────────────────────────────────────────────────────────────
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'config.middleware.LoggingMiddleware',
]

ROOT_URLCONF = 'config.urls'

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

WSGI_APPLICATION = 'config.wsgi.application'

# ─── Base de datos ────────────────────────────────────────────────────────────
DB_SCHEMA = env('DB_SCHEMA', default='ventas_schema')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('DB_NAME'),
        'USER': env('DB_USER'),
        'PASSWORD': env('DB_PASSWORD'),
        'HOST': env('DB_HOST'),
        'PORT': env('DB_PORT'),
        'OPTIONS': {
            'options': f'-c search_path={DB_SCHEMA},public'
        },
    }
}

# ─── Contraseñas ─────────────────────────────────────────────────────────────
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ─── Internacionalización ─────────────────────────────────────────────────────
LANGUAGE_CODE = 'es-co'
TIME_ZONE = 'America/Bogota'
USE_I18N = True
USE_TZ = True

# ─── Archivos estáticos ───────────────────────────────────────────────────────
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ─── Django REST Framework ────────────────────────────────────────────────────
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
    'DEFAULT_PAGINATION_CLASS': 'config.pagination.StandardPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'EXCEPTION_HANDLER': 'config.exceptions.custom_exception_handler',
}

# ─── JWT ──────────────────────────────────────────────────────────────────────
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(
        minutes=env.int('JWT_ACCESS_TOKEN_LIFETIME_MINUTES', default=60)
    ),
    'REFRESH_TOKEN_LIFETIME': timedelta(
        days=env.int('JWT_REFRESH_TOKEN_LIFETIME_DAYS', default=7)
    ),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'AUTH_HEADER_TYPES': ('Bearer',),
}

# ─── Swagger / drf-spectacular ────────────────────────────────────────────────
SPECTACULAR_SETTINGS = {
    'TITLE': 'API Sistema de Gestión de Ventas',
    'DESCRIPTION': (
        'API REST para administrar clientes, productos, proveedores, '
        'pedidos, facturas, pagos y sucursales. '
        'Desarrollado con Django REST Framework.'
    ),
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'COMPONENT_SPLIT_REQUEST': True,

    # Hace que Swagger recuerde el login
    'SWAGGER_UI_SETTINGS': {
        'persistAuthorization': True,
    },

    # Esquema global de seguridad JWT
    'SECURITY': [
        {
            'jwtAuth': []
        }
    ],

    # Definición del esquema Bearer JWT
    'APPEND_COMPONENTS': {
        'securitySchemes': {
            'jwtAuth': {
                'type': 'http',
                'scheme': 'bearer',
                'bearerFormat': 'JWT',
            }
        }
    },

    'TAGS': [
        {'name': 'Autenticación', 'description': 'Login, registro y JWT'},
        {'name': 'Clientes', 'description': 'CRUD de clientes'},
        {'name': 'Productos', 'description': 'CRUD de productos'},
        {'name': 'Proveedores', 'description': 'CRUD de proveedores'},
        {'name': 'Sucursales', 'description': 'CRUD de sucursales'},
        {'name': 'Pedidos', 'description': 'CRUD de pedidos'},
        {'name': 'Detalle Pedidos', 'description': 'CRUD de detalle de pedidos'},
        {'name': 'Facturas', 'description': 'CRUD de facturas'},
        {'name': 'Pagos', 'description': 'CRUD de pagos'},
    ],
}

# ─── Logging ──────────────────────────────────────────────────────────────────
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '[{asctime}] {levelname} {name} - {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs' / 'ventas_api.log',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'api': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
        'django.request': {
            'handlers': ['console', 'file'],
            'level': 'ERROR',
            'propagate': False,
        },
    },
}
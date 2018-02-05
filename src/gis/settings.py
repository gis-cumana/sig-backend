import os
from os.path import dirname, join, exists


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MEDIA_ROOT = os.path.join(BASE_DIR, 'media').replace('\\', '/')

MEDIA_URL = '/media/'  

SECRET_KEY = 'e*2n!dvk%g5_h_5x)=18l052_!4utghy6+$eg*z7*z9c9x-)c)'

DEBUG = True

ALLOWED_HOSTS = ["*", "127.0.0.1"]

CORS_ORIGIN_ALLOW_ALL = True

FILE_UPLOAD_HANDLERS = {
    'django.core.files.uploadhandler.TemporaryFileUploadHandler',
}

AUTHENTICATION_BACKENDS = (
    
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # allauth specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend'
    
)


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'django.contrib.gis',
    'capas.apps.CapasConfig',
    'rest_framework.authtoken',
    'rest_auth',
    'django.contrib.auth',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'rest_auth.registration',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.facebook',     
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.twitter',
    
]

SITE_ID = 2

MIDDLEWARE = [  
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',    

]

ROOT_URLCONF = 'gis.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            join(BASE_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [

                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',                                
            ],
            
        },

    },
]

WSGI_APPLICATION = 'gis.wsgi.application'

DATABASES = {
        'default': {
            'ENGINE': 'django.contrib.gis.db.backends.postgis', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
            'NAME': 'gis',                      # Or path to database file if using sqlite3.
            # The following settings are not used with sqlite3:
            'USER': 'postgres',
            'PASSWORD': '123457',
            'HOST': 'localhost',                      # Empty for localhost through domain sockets or           '127.0.0.1' for localhost through TCP.
            'PORT': '5432',                      # Set to empty string for default.
        }
    }

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
     'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
    )
}


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



LANGUAGE_CODE = 'es-AR'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'


""" CONFIGURACION ADICIONAL DE AUTH PARA EL MODELO DE USUARIOS """
""" PARA LA ACTUALIZACION Y REGISTROS DE USUARIOS """

""" SERIALIZER UPDATE LOCAL ACCOUNT"""
REST_AUTH_SERIALIZERS = {
    'USER_DETAILS_SERIALIZER': 'capas.serializadores.UserSerializer',   

}



""" AGREGAMOS ESTOS CAMPOS PARA PERMITIR LA VERIFICACION POR EMAIL """

#ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_EMAIL_VERIFICATION = "none"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_AUTHENTICATION_METHOD = 'email'
SOCIALACCOUNT_QUERY_EMAIL = True
LOGIN_REDIRECT_URL = "/"

""" CONFIGURACION PARA SOCIAL ACCOUNT """
SOCIALACCOUNT_PROVIDERS = {
    'facebook':
        {
            'METHOD': 'js_sdk',
            'SCOPE': ['email',],
            
        },
    'google':
        {
            'SCOPE': [ 'profile', 'email', ],
            'AUTH_PARAMS': { 'access_type': 'online', }
        }
    } 

SOCIAL_AUTH_FACEBOOK_KEY = '108416949950283'  # App ID
SOCIAL_AUTH_FACEBOOK_SECRET ='19114b1c0aaf3ba2e2328fcc7fd0e8be' #app key
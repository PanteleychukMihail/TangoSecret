import os.path
from pathlib import Path

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('SECRET_KEY')

DEBUG = True if os.getenv('DEBUG', 'false').lower() in ('1', 'true') else False

ALLOWED_HOSTS = [os.getenv('DJANGO_ALLOWED_HOSTS')]


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv('POSTGRES_DB'),
        'USER': 'userdb',
        'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
        'HOST': os.getenv('POSTGRES_HOST'),
        'PORT': os.getenv('POSTGRES_PORT')
    }
}




STATIC_DIR = os.path.join(BASE_DIR, 'tangoschool/../tangoschool/static')
STATICFILES_DIRS = []
STATIC_ROOT = os.path.join(BASE_DIR, 'tangoschool/../tangoschool/static')

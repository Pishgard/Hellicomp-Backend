# Sqlite
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Postgres
# DATABASES = {
#   'default': {
#     'ENGINE': 'django.db.backends.postgresql',
#     'HOST': 'postgres',
#     'NAME': 'kgoo_db',
#     'USER': 'root',
#     'PASSWORD': 'Heysite@2022',
#   }
# }

# Mysql
# import os
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'kgoo_db',
#         'USER': 'root',
#         'PASSWORD': 'Heysite@2022',
#         'HOST': 'mysql',
#         'PORT': '3306'
#     }
# }

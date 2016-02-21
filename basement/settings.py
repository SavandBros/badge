# -*- coding: utf-8 -*-
import os

from redis import Redis

PYPI_URL = "https://pypi.python.org/pypi/%s/json"

FILE_CACHE = "/tmp/badge.py/"
CACHE_TIME = (60 * 60) * 24  # 24 hours
REDIS_EXPIRE = 60 * 10  # 10 minutes
BASE_DIR = PROJECT_DIR = os.path.abspath(os.path.join(
    os.path.dirname(__file__),
    os.path.pardir)
)

STATIC_DIR = os.path.join(BASE_DIR, 'static/')
TEMPLATE_DIR_NAME = 'templates'
TEMPLATES_DIR = os.path.join(BASE_DIR, TEMPLATE_DIR_NAME)

ALLOWED_EXTENSIONS = (
    'png',
    'svg'
)

redis = Redis()

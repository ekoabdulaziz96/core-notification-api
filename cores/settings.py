# -*- coding: utf-8 -*-
import logging

from environs import Env

env = Env()
env.read_env()

FLASK_APP = env.str("FLASK_APP", default="server.py")
ENV = env.str("FLASK_ENV", default="production")
DEBUG = ENV == "development"
TIMEZONE = env.str("TIMEZONE", default="Asia/Jakarta")
TIMEZONE_ADD_HOUR = env.int("TIMEZONE_ADD_HOUR_FROM_UTC", default=7)

LOG_LEVEL = logging.INFO
if DEBUG:
    LOG_LEVEL = logging.DEBUG

# flask-sqlalchemy config
SQLALCHEMY_DATABASE_URI = env.str("SQLALCHEMY_DATABASE_URI", default=None)
SQLALCHEMY_TRACK_MODIFICATIONS = False

# flask-caching config
CACHE_TYPE = "RedisCache"  # Flask-Caching related configs
CACHE_DEFAULT_TIMEOUT = 600  # seconds -> 10 minutes
CACHE_REDIS_URL = env.str("CACHE_REDIS_URL", default=None)

CELERY_TIMEZONE = env.str("CELERY_TIMEZONE", "Asia/Jakarta")
CELERY_BROKER_URL = env.str("CELERY_BROKER_URL", "redis://localhost:6379/0")
CELERY_RESULT_BACKEND = env.str("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")
CELERY_SEND_SENT_EVENT = True

SENTRY_DSN = env.str("SENTRY_DSN", default=None)
SENTRY_ENV = ENV
SENTRY_TURN_OFF = env.str("SENTRY_TURN_OFF", default="False") == "True"

MAIL_SERVER = "smtp.gmail.com"
MAIL_PORT = 465
MAIL_USERNAME = env.str("MAIL_USERNAME", default=None)
MAIL_PASSWORD = env.str("MAIL_PASSWORD", default=None)
MAIL_DEFAULT_SENDER = env.str("MAIL_DEFAULT_SENDER", default=None)
MAIL_USE_TLS = False
MAIL_USE_SSL = True

EMAIL_TIMESTAMP_THRESHOLD = env.int("EMAIL_TIMESTAMP_THRESHOLD", default=1)     # minutes

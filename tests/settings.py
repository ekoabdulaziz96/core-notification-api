"""Settings module for test app."""

FLASK_APP = "server.py"
SECRET_KEY = "not-so-secret-in-tests"
ENV = "development"
TESTING = True
DEBUG = ENV == "development"
TIMEZONE = "Asia/Singapore"
DEBUG_TB_ENABLED = False
WTF_CSRF_ENABLED = False  # Allows form testing

BCRYPT_LOG_ROUNDS = 4  # For faster tests; needs at least 4 to avoid "ValueError: Invalid rounds"

# flask-sqlalchemy config
SQLALCHEMY_DATABASE_URI = "sqlite://"
SQLALCHEMY_TRACK_MODIFICATIONS = False

# flask-caching config
CACHE_TYPE = "flask_caching.backends.SimpleCache"  # Can be "memcached", "redis", etc.
CACHE_DEFAULT_TIMEOUT = 60  # seconds -> 10 minutes

CELERY_TIMEZONE = "Asia/Singapore"
CELERY_BROKER_URL = "redis://"
CELERY_RESULT_BACKEND = "redis://"
CELERY_SEND_SENT_EVENT = True

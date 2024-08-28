"""Extensions module. Each extension is initialized in the app factory located in app.py."""

import alembic_postgresql_enum  # noqa
from flask_bcrypt import Bcrypt
from flask_caching import Cache
from flask_mail import Mail
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy


db: SQLAlchemy = SQLAlchemy()
migrate = Migrate()
ma = Marshmallow()

mail = Mail()
cache = Cache()
bcrypt = Bcrypt()


# NOTE:
# flask_sqlalchemy      : https://flask-migrate.readthedocs.io/en/latest/
# flask_migrate         : https://flask-migrate.readthedocs.io/en/latest/
# flask_marshmallow     : https://flask-marshmallow.readthedocs.io/en/latest/
# flask_mail            : https://pythonhosted.org/Flask-Mail/
# flask_caching         : https://flask-caching.readthedocs.io/en/latest/
# celery                : https://docs.celeryq.dev/en/stable/index.html
# flask_bcrypt          : https://flask-bcrypt.readthedocs.io/en/1.0.1/
# alembic_postgresql_enum: https://github.com/Pogchamp-company/alembic-postgresql-enum

from celery import Celery
from flask import Flask

from cores import extensions, settings
from models._register_tables import register_tables
from urls._register_routers import blueprints


def create_app(config_object=settings, testing=None):
    """
    Create application factory,
    as explained here: http://flask.pocoo.org/docs/patterns/appfactories/.
    :param config_object: The configuration object to use.
    """
    app = Flask(__name__)
    app.config.from_object(config_object)
    app.logger.setLevel(settings.LOG_LEVEL)
    register_blueprints(app)
    register_extensions(app)
    register_shellcontext(app)
    register_commands(app)

    if testing:
        app.testing=testing

    return app


def create_worker_app(config_object=settings):
    """create worker app without blueprint"""

    app = Flask(__name__)
    app.config.from_object(config_object)
    app.logger.setLevel(settings.LOG_LEVEL)
    register_extensions(app)
    register_shellcontext(app)

    return app


def register_extensions(app):
    """Register Flask extensions."""

    extensions.db.init_app(app)
    extensions.migrate.init_app(app, extensions.db)
    extensions.ma.init_app(app)
    extensions.cache.init_app(app)
    extensions.mail.init_app(app)
    if not app.testing:
        extensions.admin.init_app(app)


def register_blueprints(app):
    """Register Flask blueprints."""
    for blueprint in blueprints:
        app.register_blueprint(blueprint)
        
    if not app.testing:
        from admins._register_views import bp_admins
        app.register_blueprint(bp_admins)


def register_shellcontext(app):
    """Register shell context objects."""

    shell_context = {"db": extensions.db}
    shell_context.update(register_tables)

    app.shell_context_processor(lambda: shell_context)


def register_commands(app):
    """Register Click commands."""
    pass


def make_celery(app):
    celery = Celery(
        "core_notif",
        broker=app.config["CELERY_BROKER_URL"],
        result_backend=app.config["CELERY_RESULT_BACKEND"],
        include=["tasks.workers"],
        enable_utc=True,
        timezone=app.config["CELERY_TIMEZONE"],
        broker_connection_retry_on_startup=True,
    )

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery

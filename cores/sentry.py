from flask import current_app
from sentry_sdk import init as SentrySDK
from sentry_sdk.integrations.flask import FlaskIntegration

from cores import settings

if not settings.SENTRY_TURN_OFF and not current_app.testing:  # pragma: no cover
    SentrySDK(
        dsn=settings.SENTRY_DSN,
        environment=settings.SENTRY_ENV,
        send_default_pii=True,
        integrations=[
            FlaskIntegration(
                transaction_style="url",
            ),
        ],
    )

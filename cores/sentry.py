from flask import current_app
from sentry_sdk import (
    capture_exception,
    init as SentrySDK,
    isolation_scope,
)
from sentry_sdk.integrations.flask import FlaskIntegration

from cores import settings

if not settings.SENTRY_TURN_OFF and not current_app.testing:    # pragma: no cover
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


def capture_rest_api_exception(exception):
    if current_app.testing:
        print(f"ERROR_SYSTEM: {str(exception)}")
        return

    if settings.SENTRY_TURN_OFF:
        raise exception
        # print(exception)

    with isolation_scope() as scope:  # pragma: no cover
        scope.level = "warning"
        scope.set_extra("original_exception", str(exception))
        capture_exception(exception)

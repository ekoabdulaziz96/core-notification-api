from flask import current_app
from sentry_sdk import capture_exception, isolation_scope

from cores import settings


def capture_rest_api_exception(exception):
    if current_app.testing:
        print(f"ERROR_SYSTEM: {str(exception)}")
        return

    elif settings.SENTRY_TURN_OFF:
        raise exception
        # print(exception)

    with isolation_scope() as scope:  # pragma: no cover
        scope.level = "warning"
        scope.set_extra("original_exception", str(exception))
        capture_exception(exception)


class CustomBaseException(BaseException):
    error_code = None
    error_cause = None

    def __init__(self, message=None, **kwargs):
        self.message = message
        self.__dict__.update(kwargs)
        BaseException().__init__(self, message)


class ValidationException(CustomBaseException):
    pass


class ModuleEmailException(CustomBaseException):
    pass

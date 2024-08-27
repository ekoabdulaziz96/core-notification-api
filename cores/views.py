from constants.messages import resp_err
from cores.exceptions import ValidationException


class BaseView:
    """abstract class controller for handle request"""

    def __init__(self, request, **kwargs):
        self.kwargs = kwargs
        self.request = request
        self.headers = request.headers if request.headers else {}

    def _validate_header_json(self):
        if self.headers.get("Content-Type", None) != "application/json":
            raise ValidationException(error_code=resp_err.invalid_header_json)

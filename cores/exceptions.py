class CustomBaseException(BaseException):
    error_code = None
    error_cause = None

    def __init__(self, message=None, **kwargs):
        self.message = message
        self.__dict__.update(kwargs)
        BaseException().__init__(self, message)


class ValidationException(CustomBaseException):
    pass

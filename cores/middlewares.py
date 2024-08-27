from flask import request
from marshmallow import ValidationError

from constants.messages import resp_err
from cores.databases import db
from cores.exceptions import ValidationException
from cores.responses import Response
from cores.sentry import capture_rest_api_exception


class Middleware:
    @classmethod
    def process(cls, view_class, view_method, **kwargs):
        db.session.begin()
        try:
            response_data, response_code = view_class(request, **kwargs).__getattribute__(view_method)()
            response, status_code = Response().process_response_success(response_code, response_data)

            db.session.commit()

        except ValidationError as err:
            response, status_code = Response().process_response_error(resp_err.invalid_request_data, data=err.messages)

        except ValidationException as err:
            response, status_code = Response().process_response_error(err.error_code, message=err.message)

        except Exception as err:
            capture_rest_api_exception(err)

            db.session.rollback()

            response, status_code = Response().process_response_error(resp_err.error_system, message=None)

        finally:
            db.session.close()

        return response, status_code


middleware = Middleware()

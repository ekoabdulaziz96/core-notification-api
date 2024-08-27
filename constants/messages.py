from constants import status


class ResponseError:
    error_system = "ERROR_SYSTEM"
    invalid_header_json = "INVALID_HEADER_JSON"
    invalid_request_param = "INVALID_REQUEST_PARAM"
    invalid_request_data = "INVALID_REQUEST_DATA"
    data_not_found = "DATA_NOT_FOUND"


class ResponseSuccess:
    success = "SUCCESS"
    success_create = "SUCCESS_CREATE"
    success_update = "SUCCESS_UPDATE"
    success_delete = "SUCCESS_DELETE"


resp_err = ResponseError()
resp_success = ResponseSuccess()

RESPONSE_ERROR = {
    resp_err.error_system: {
        "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
        "code": resp_err.error_system,
        "message": "The request could not be processed. Please wait for some time before trying again. If you still have problems, contact CS 12345.",
    },
    resp_err.invalid_header_json: {
        "status_code": status.HTTP_400_BAD_REQUEST,
        "code": resp_err.invalid_header_json,
        "message": "The request could not be processed. Make sure the data you send is in json format.",
    },
    resp_err.invalid_request_param: {
        "status_code": status.HTTP_400_BAD_REQUEST,
        "code": resp_err.invalid_request_param,
        "message": "The request could not be processed. Please correct your input data.",
    },
    resp_err.invalid_request_data: {
        "status_code": status.HTTP_400_BAD_REQUEST,
        "code": resp_err.invalid_request_data,
        "message": "The request could not be processed. Please correct your input data.",
    },
    resp_err.data_not_found: {
        "status_code": status.HTTP_400_BAD_REQUEST,
        "code": resp_err.data_not_found,
        "message": "The request could not be processed. Please correct your input data.",
    },
}

RESPONSE_SUCCESS = {
    resp_success.success: {
        "status_code": status.HTTP_200_OK,
        "code": resp_success.success,
        "message": "Request successfully processed.",
    },
    resp_success.success_create: {
        "status_code": status.HTTP_201_CREATED,
        "code": resp_success.success_create,
        "message": "Request successfully processed.",
    },
    resp_success.success_update: {
        "status_code": status.HTTP_200_OK,
        "code": resp_success.success_update,
        "message": "Request successfully processed.",
    },
    resp_success.success_delete: {
        "status_code": status.HTTP_200_OK,
        "code": resp_success.success_delete,
        "message": "Request successfully processed.",
    },
}


class MessageInvalid:
    MIN_POSITIVE_VALUE = "Input value must be greater than 0."
    TIMESTAMP_FORMAT = "Please check your Timestamp format 'Day Month Year Hour:Minute', ex: '15 Dec 2015 23:12'."
    TIMESTAMP_THRESHOLD = "Please set the timestamp value at least {} minutes earlier. Now: {}."
    INVALID_EXIST_DATA = "{} already registered."
    INVALID_NOT_FOUND = "{} not found."


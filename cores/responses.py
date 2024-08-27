from datetime import datetime

from flask import jsonify

from constants.messages import RESPONSE_ERROR, RESPONSE_SUCCESS
from cores.settings import TIMEZONE
from cores.utils import generate_api_call_id, get_timezone


class Response:
    def __init__(self, status="SUCCESS", message="init-state", data=None, status_code=200):
        self.call_id = generate_api_call_id()
        self.now = datetime.now(get_timezone(TIMEZONE))
        self.status = status
        self.data = data
        self.message = message
        self.status_code = status_code

    def _response_json(self):
        return jsonify(
            {
                "request_id": self.call_id,
                "status": self.status,
                "message": self.message,
                "data": self.data,
                "request_datetime": self.now.strftime("%Y-%m-%d %H:%M:%S"),
            }
        )

    def process_response_error(self, message_code, message=None, data=None):
        response_config = RESPONSE_ERROR[message_code]

        self.status = response_config["code"]
        self.message = message or response_config["message"]
        self.status_code = response_config["status_code"]
        self.data = data or {}

        return self._response_json(), self.status_code

    def process_response_success(self, message_code, data=None):
        response_success = RESPONSE_SUCCESS[message_code]

        self.status = response_success["code"]
        self.message = response_success["message"]
        self.status_code = response_success["status_code"]
        self.data = data or {}

        return self._response_json(), self.status_code

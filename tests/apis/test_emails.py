from datetime import datetime, timedelta
from json import dumps
from random import randint, seed
from unittest import mock, TestCase

from flask import url_for
from pytest import mark

from constants import status, variables
from tests.factories import EmailFactory, faker


@mark.usefixtures("client_test")
class TestCreateUser(TestCase):
    @classmethod
    def setUpClass(cls):
        seed(1)

    def setUp(self):
        self.headers = {"Content-Type": "application/json"}
        self.payload = {
            "event_id": randint(1, 999999),
            "email_subject": "TEST IN PYTEST",
            "email_content": "Hello, you get a message from core-notif.",
            "timestamp": (datetime.now() + timedelta(hours=2)).strftime(variables.EMAIL_TIMESTAMP_FORMAT),
        }
        self.complete_url = url_for("emails.save-emails")

    @classmethod
    def tearDownClass(cls):
        cls.db.session.commit()

    def test_fail_because_header_not_json(self):
        response = self.client_app.post(self.complete_url, data=dumps({}), headers={})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json["status"], "INVALID_HEADER_JSON")
        self.assertEqual(
            response.json["message"],
            "The request could not be processed. Make sure the data you send is in json format.",
        )

    def test_fail_because_empty_payload(self):
        response = self.client_app.post(self.complete_url, data=dumps({}), headers=self.headers)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(response.json["data"]), 4)
        self.assertIn("event_id", response.json["data"].keys())
        self.assertIn("email_subject", response.json["data"].keys())
        self.assertIn("email_content", response.json["data"].keys())
        self.assertIn("timestamp", response.json["data"].keys())

    @mock.patch("views.emails.EmailSerializer.is_valid")
    def test_fail_because_server_error(self, mock_convert_datetime):
        mock_convert_datetime.side_effect = Exception("Error System")
        response = self.client_app.post(self.complete_url, data=dumps({}), headers=self.headers)

        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertEqual(response.json["status"], "ERROR_SYSTEM")
        self.assertEqual(
            response.json["message"],
            "The request could not be processed. Please wait for some time before trying again."
            + " If you still have problems, contact CS 12345.",
        )

    def test_fail_because_invalid_event_id_format(self):
        self.payload["event_id"] = "random"
        response = self.client_app.post(self.complete_url, data=dumps(self.payload), headers=self.headers)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(response.json["data"]), 1)
        self.assertEqual(response.json["data"]["event_id"][0], "Not a valid integer.")

    def test_fail_because_invalid_event_id_for_negative_value(self):
        self.payload["event_id"] = -99
        response = self.client_app.post(self.complete_url, data=dumps(self.payload), headers=self.headers)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(response.json["data"]), 1)
        self.assertEqual(response.json["data"]["event_id"][0], "Input value must be greater than 0.")

    def test_fail_because_event_id_already_exist(self):
        email_data = EmailFactory()
        self.payload["event_id"] = email_data.event_id
        response = self.client_app.post(self.complete_url, data=dumps(self.payload), headers=self.headers)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(response.json["data"]), 1)
        self.assertEqual(response.json["data"]["event_id"][0], "Event ID already registered.")

    def test_fail_because_exceeded_max_email_subject(self):
        self.payload["email_subject"] = faker.text(max_nb_chars=500)[:110]
        response = self.client_app.post(self.complete_url, data=dumps(self.payload), headers=self.headers)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(response.json["data"]), 1)
        self.assertEqual(response.json["data"]["email_subject"][0], "Longer than maximum length 100.")

    def test_fail_because_invalid_timestamp_format(self):
        self.payload["timestamp"] = "2024-08-07 13:00"
        response = self.client_app.post(self.complete_url, data=dumps(self.payload), headers=self.headers)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(response.json["data"]), 1)
        self.assertEqual(
            response.json["data"]["timestamp"][0],
            "Please check your Timestamp format 'Day Month Year Hour:Minute', ex: '15 Dec 2015 23:12'.",
        )

    def test_fail_because_invalid_timestamp_threshold(self):
        self.payload["timestamp"] = "15 Dec 2015 23:12"
        response = self.client_app.post(self.complete_url, data=dumps(self.payload), headers=self.headers)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(response.json["data"]), 1)
        self.assertIn(
            "Please set the timestamp value at least 5 minutes earlier.", response.json["data"]["timestamp"][0]
        )

    def test_success(self):
        response = self.client_app.post(self.complete_url, data=dumps(self.payload), headers=self.headers)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json["data"]
        self.assertEqual(response_data["email_subject"], "TEST IN PYTEST")
        self.assertEqual(response_data["email_content"], "Hello, you get a message from core-notif.")
        self.assertEqual(response_data["timestamp"], self.payload["timestamp"])
        self.assertEqual(response_data["status"], "pending")
        self.assertEqual(len(response_data), 5)

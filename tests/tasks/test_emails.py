from datetime import datetime, timedelta
from unittest import mock, TestCase

from pytest import mark
from sqlalchemy import update

from cores.exceptions import ModuleEmailException
from cores.utils import get_timezone
from models.emails import EmailHistoryQuery, EmailHistoryStatusChoices, EmailStatusChoices
from tasks.workers import task_send_email
from tests.factories import EmailFactory, UserRecipient, UserRecipientFactory


@mark.usefixtures("client_test")
class TestTaskSendEmail(TestCase):
    def setUp(self):
        self.timezone = get_timezone()
        self.now = datetime.now(tz=self.timezone).replace(second=0, microsecond=0)
        self.email = EmailFactory(timestamp=self.now)

        self.user_recipients = UserRecipientFactory.create_batch(2)

    @classmethod
    def tearDownClass(cls):
        cls.db.session.commit()

    def test_fail_because_no_active_recipient(self):
        self.db.session.execute(update(UserRecipient).values(is_active=False))
        self.db.session.commit()

        with self.assertRaises(ModuleEmailException) as err:
            task_send_email()

        self.assertEqual(self.email.status, EmailStatusChoices.PENDING)
        self.assertEqual(str(err.exception), "No active user recipients.")

    @mock.patch("flask_mail.Connection.send")
    def test_fail_because_error_connection(self, mock_send_email):
        mock_send_email.side_effect = ConnectionError("error server, 500")

        email_2 = EmailFactory(timestamp=self.now)
        self.assertEqual(self.email.status, EmailStatusChoices.PENDING)
        self.assertEqual(email_2.status, EmailStatusChoices.PENDING)

        task_send_email()

        self.db.session.refresh(self.email)
        self.db.session.refresh(email_2)
        self.assertEqual(self.email.status, EmailStatusChoices.FAILED)
        self.assertEqual(email_2.status, EmailStatusChoices.FAILED)

        self.assertTrue(mock_send_email.called)

        with self.subTest("check email history"):
            for email in [self.email, email_2]:
                email_history = EmailHistoryQuery.get_by_email_id(email.id)
                self.assertEqual(email_history.status, EmailHistoryStatusChoices.FAILED)
                self.assertEqual(email_history.err_message, "error server, 500")

    def test_success_with_no_email_send(self):
        self.email.timestamp = self.now + timedelta(minutes=1)
        self.email.save()
        self.assertEqual(self.email.status, EmailStatusChoices.PENDING)

        task_send_email()

        self.db.session.refresh(self.email)
        self.assertEqual(self.email.status, EmailStatusChoices.PENDING)

    @mock.patch("flask_mail.Connection.send")
    def test_success_send_email(self, mock_send_email):
        mock_send_email.return_value = "success"

        email_2 = EmailFactory(timestamp=self.now)
        self.assertEqual(self.email.status, EmailStatusChoices.PENDING)
        self.assertEqual(email_2.status, EmailStatusChoices.PENDING)

        task_send_email()

        self.db.session.refresh(self.email)
        self.db.session.refresh(email_2)
        self.assertEqual(self.email.status, EmailStatusChoices.SUCCESS)
        self.assertEqual(email_2.status, EmailStatusChoices.SUCCESS)

        self.assertTrue(mock_send_email.called)

        with self.subTest("check email history"):
            for email in [self.email, email_2]:
                email_history = EmailHistoryQuery.get_by_email_id(email.id)
                self.assertEqual(email_history.status, EmailHistoryStatusChoices.SUCCESS)
                self.assertIsNone(email_history.err_message)

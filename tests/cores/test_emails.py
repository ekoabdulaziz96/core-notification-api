from unittest import skip, TestCase

from cores.extensions import mail
from server import app


@skip("only check test for real server")
class TestMailConnection(TestCase):  # pragma: no cover
    @classmethod
    def setUpClass(cls):
        super(TestMailConnection, cls).setUpClass()

        # instance app Flask and client
        cls.app = app
        cls.app.debug = True
        cls.client = cls.app.test_client()

    def test_success_mail(self):
        #  https://pythonhosted.org/Flask-Mail/#unit-tests-and-suppressing-emails
        with mail.record_messages() as outbox:
            with self.app.app_context():
                mail.send_message(subject="testing", body="test", recipients=["azizeko29undip@gmail.com"])

            assert len(outbox) == 1
            assert outbox[0].subject == "testing"

from typing import List

from flask_mail import Message

from cores.exceptions import ModuleEmailException
from cores.extensions import mail
from models.emails import Email, EmailHistory, EmailHistoryStatusChoices, EmailStatusChoices, UserRecipientQuery


class ModuleEmail:
    def _send_email(self, email: Email):
        email_recipients = UserRecipientQuery.get_all_of_email_from_active_recipient()
        if not email_recipients:
            raise ModuleEmailException("No active user recipients.")

        email.update(status=EmailStatusChoices.PROCESS)
        email_history = EmailHistory(
            email=email, email_recipients=str(email_recipients), status=EmailHistoryStatusChoices.PROCESS
        )
        email_history.save()

        with mail.connect() as conn:
            try:
                msg = Message(recipients=email_recipients, body=email.email_content, subject=email.email_subject)
                conn.send(msg)

                email_history.update(status=EmailHistoryStatusChoices.SUCCESS)
                email.update(status=EmailStatusChoices.SUCCESS)

            except Exception as err:
                email_history.update(
                    status=EmailHistoryStatusChoices.FAILED, err_message=str(err)[: EmailHistory.MAX_MESSAGE]
                )
                email.update(status=EmailStatusChoices.FAILED)

    def process_send_email(self, emails: List[Email]):
        for email in emails:
            self._send_email(email)


module_email = ModuleEmail()

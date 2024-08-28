from datetime import datetime
from enum import Enum
from typing import List

from cores.databases import Column, db, PkModelWithManageAttr, reference_col
from cores.utils import get_timezone


class EmailStatusChoices(Enum):
    PENDING = "pending"
    PROCESS = "process"
    SUCCESS = "success"
    FAILED = "failed"


class Email(PkModelWithManageAttr):
    __tablename__ = "emails"
    MAX_EMAIL_SUBJECT = 100

    event_id = Column(db.Integer, nullable=False, unique=True)
    email_subject = Column(db.String(MAX_EMAIL_SUBJECT), nullable=False)
    email_content = Column(db.Text, nullable=False)
    timestamp = Column(db.DateTime(timezone=True), nullable=False)

    status = Column("status", db.Enum(EmailStatusChoices, name="email_status_choices_enum"))

    __table_args__ = (
        db.Index("email_idx_for_time_and_status", timestamp.asc(), status),
        db.Index("email_idx_for_email_id", event_id, postgresql_using="hash"),
    )

    def __repr__(self):  # pragma: no cover
        return f"EMAIL [{self.id}] {self.email_subject[:25]}..."


class UserRecipient(PkModelWithManageAttr):
    __tablename__ = "user_recipients"
    MAX_EMAIL = 50

    email = Column(db.String(MAX_EMAIL), nullable=False, unique=True)
    is_active = Column(db.Boolean(), default=False)

    def __repr__(self):  # pragma: no cover
        return f"USER_RECIPIENT [{self.id}] {self.email}"


class EmailHistoryStatusChoices(Enum):
    PENDING = "pending"
    PROCESS = "process"
    SUCCESS = "success"
    FAILED = "failed"


class EmailHistory(PkModelWithManageAttr):
    __tablename__ = "email_histories"
    MAX_MESSAGE = 255

    status = Column("status", db.Enum(EmailHistoryStatusChoices, name="email_history_status_choices_enum"))
    email_recipients = Column(db.Text, nullable=True)
    err_message = Column(db.String(MAX_MESSAGE), nullable=True)

    email_id = reference_col("emails", nullable=False)
    email = db.relationship('Email', backref='email_history', uselist=False, lazy=True)

    def __repr__(self):  # pragma: no cover
        return f"EMAIL_HISTORY [{self.email_id}] {self.email_recipients[:20]}..."


# ---------------------------------------------------------------------------- Query class
class EmailQuery:
    @classmethod
    def get_by_event_id(cls, event_id: str) -> int:
        return Email.query.filter_by(event_id=event_id).count()

    @classmethod
    def get_all_by_current_datetime(cls) -> List[Email]:
        timezone = get_timezone()
        dt_now = datetime.now(tz=timezone).replace(second=0, microsecond=0)

        return Email.query.filter_by(timestamp=dt_now).filter_by(status=EmailStatusChoices.PENDING).all()


class UserRecipientQuery(object):
    @classmethod
    def get_all_of_email_from_active_recipient(cls) -> List[str]:
        query_emails = UserRecipient.query.filter_by(is_active=True).with_entities(UserRecipient.email).all()
        if not query_emails:
            return []

        return [email[0] for email in query_emails]


class EmailHistoryQuery(object):
    @classmethod
    def get_by_email_id(cls, email_id: str) -> List[EmailHistory]:
        return EmailHistory.query.filter_by(email_id=email_id).first()

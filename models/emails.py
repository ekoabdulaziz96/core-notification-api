from datetime import datetime, timedelta
from enum import Enum
from typing import List

from constants import variables
from cores.databases import Column, db, PkModelWithManageAttr, reference_col, relationship
from cores.utils import get_timezone


class EmailStatusChoices(Enum):
    PENDING = "pending"
    QUEUED = "queued"
    SUCCESS = "success"
    FAIL = "failed"


class Email(PkModelWithManageAttr):
    __tablename__ = "emails"
    MAX_EMAIL_SUBJECT = 100

    event_id = Column(db.Integer, nullable=False, unique=True)
    email_subject = Column(db.String(MAX_EMAIL_SUBJECT), nullable=False)
    email_content = Column(db.Text, nullable=False)
    timestamp = Column(db.DateTime(timezone=True), nullable=False)

    status = Column("status", db.Enum(EmailStatusChoices, name="email_status_choices_enum"))

    email_histories = relationship("EmailHistory", backref="email", lazy="dynamic")

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

    email_histories = relationship("EmailHistory", backref="user_recipient", lazy="dynamic")

    def __repr__(self):  # pragma: no cover
        return f"USER_RECIPIENT [{self.id}] {self.email}"


class EmailHistoryStatusChoices(Enum):
    PENDING = "pending"
    QUEUED = "queued"
    SUCCESS = "success"
    FAIL = "failed"


class EmailHistory(PkModelWithManageAttr):
    __tablename__ = "email_histories"
    MAX_MESSAGE = 255

    status = Column("status", db.Enum(EmailHistoryStatusChoices, name="email_history_status_choices_enum"))
    err_message = Column(db.String(MAX_MESSAGE), nullable=True)

    # many to one relations
    email_id = reference_col("emails", nullable=False)
    user_recipient_id = reference_col("user_recipients", nullable=False)

    def __repr__(self):  # pragma: no cover
        return f"EMAIL_HISTORY [{self.history_id}]"


# ---------------------------------------------------------------------------- Query class
class EmailQuery:
    @classmethod
    def get_by_event_id(cls, event_id: str) -> int:
        return Email.query.filter_by(event_id=event_id).count()

    @classmethod
    def get_all_by_email_subject(cls, email_subject: str) -> List[Email]:
        return Email.query.filter_by(email_subject=email_subject).all()

    @classmethod
    def get_all_by_current_datetime(cls, timezone="Asia/Jakarta") -> List[Email]:
        """read all data filter by `datetime_now`
        :datetime_now -> datetime_now value for filter data
        """
        tz_singapore = get_timezone(timezone)
        dt_now_str = (datetime.now(tz=tz_singapore) - timedelta(hours=8)).strftime(variables.EMAIL_TIMESTAMP_FORMAT)
        dt_now = datetime.strptime(dt_now_str, variables.EMAIL_TIMESTAMP_FORMAT)

        return Email.query.filter_by(timestamp=dt_now).filter_by(status=EmailStatusChoices.PENDING).all()


class UserRecipientQuery(object):
    @classmethod
    def get_by_recipient_id(cls, recipient_id: str) -> UserRecipient:
        return UserRecipient.query.filter_by(recipient_id=recipient_id).first()

    @classmethod
    def get_by_email(cls, email: str) -> UserRecipient:
        return UserRecipient.query.filter_by(email=email).first()

    @classmethod
    def get_all_of_active_recipient(cls) -> List[UserRecipient]:
        return UserRecipient.query.filter_by(is_active=True).all()


class EmailHistoryQuery(object):
    """Resource class for doing query data in Email Histories table"""

    @classmethod
    def get_one_filter_by_history_id(cls, history_id: str) -> EmailHistory:
        """read one data filter by `history_id`
        :history_id -> history_id value for filter data
        """
        return EmailHistory.query.filter_by(history_id=history_id).first()

    @classmethod
    def get_one_filter_by_emailID_and_userRecipientID(cls, email_id: str, user_recipient_id: str) -> EmailHistory:
        """read one data filter by `email_id` and `user_recipient_id`
        :email_id -> email_id value for filter data
        :user_recipient_id -> user_recipient_id value for filter data
        """
        return EmailHistory.query.filter_by(email_id=email_id).filter_by(user_recipient_id=user_recipient_id).first()

    @classmethod
    def get_all_filter_by_email_id(cls, email_id: str) -> List[EmailHistory]:
        """read all data filter by `email_id`
        :email_id -> email_id value for filter data
        """
        return EmailHistory.query.filter_by(email_id=email_id).all()

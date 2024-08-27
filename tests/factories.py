from datetime import datetime

from factory import Faker, Sequence
from factory.alchemy import SQLAlchemyModelFactory
from faker import Faker as FakeGenerator

from cores.extensions import db
from cores.utils import get_timezone
from models.emails import Email, EmailStatusChoices, UserRecipient

faker = FakeGenerator()

class BaseFactory(SQLAlchemyModelFactory):
    class Meta:
        abstract = True
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = "commit"


class EmailFactory(BaseFactory):
    event_id = Sequence(lambda n: int(n)+1)
    email_subject = Faker("sentence")
    email_content = Faker("sentence")
    timestamp = datetime.now(tz=get_timezone())
    status = EmailStatusChoices.PENDING

    class Meta:
        model = Email


class UserRecipientFactory(BaseFactory):
    email = Sequence(lambda n: f"user{n}@example.com")
    is_active = True

    class Meta:
        model = UserRecipient

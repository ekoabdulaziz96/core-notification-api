from datetime import datetime

from marshmallow import fields, validate, validates, validates_schema, ValidationError

from constants import variables
from constants.messages import MessageInvalid
from cores import settings
from cores.serializers import Serializer
from cores.utils import get_timezone
from models.emails import Email, EmailQuery, EmailStatusChoices


class EmailSerializer(Serializer):
    model = Email
    model_query = EmailQuery

    event_id = fields.Integer(required=True, validate=validate.Range(min=1, error=MessageInvalid.MIN_POSITIVE_VALUE))
    email_subject = fields.Str(required=True, validate=validate.Length(max=Email.MAX_EMAIL_SUBJECT))
    email_content = fields.Str(required=True)

    timestamp = fields.DateTime(
        required=True,
        format=variables.EMAIL_TIMESTAMP_FORMAT,
        error_messages={"invalid": MessageInvalid.TIMESTAMP_FORMAT},
    )
    status = fields.Function(lambda obj: obj.status.value if obj.status else obj.status, dump_only=True)

    class Meta:
        fields = ("event_id", "email_subject", "email_content", "timestamp", "status")

    @validates("event_id")
    def validate_event_id(self, value):
        if EmailQuery.get_by_event_id(value):
            raise ValidationError(MessageInvalid.INVALID_EXIST_DATA.format("Event ID"))

    @validates_schema
    def validates_data(self, data, **kwargs):
        timezone = get_timezone()
        dt_now = datetime.now(tz=timezone).replace(second=0, microsecond=0)
        dt_now_str = dt_now.strftime(variables.EMAIL_TIMESTAMP_FORMAT)

        timestamp_with_timezone = timezone.localize(data["timestamp"])

        delta_dt = (timestamp_with_timezone - dt_now).total_seconds()
        threshold = settings.EMAIL_TIMESTAMP_THRESHOLD
        if delta_dt < threshold * 60:
            raise ValidationError(
                MessageInvalid.TIMESTAMP_THRESHOLD.format(threshold, dt_now_str), field_name="timestamp"
            )

        data["timestamp"] = timestamp_with_timezone
        return data

    def is_valid(self, payload):
        self.validated_data = self.load(payload)
        self.validated_data["status"] = EmailStatusChoices.PENDING

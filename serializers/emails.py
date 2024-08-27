from datetime import datetime

from marshmallow import fields, validate, validates, validates_schema, ValidationError

from constants import variables as const
from constants.messages import MessageInvalid
from cores import settings
from cores.serializers import Serializer
from cores.utils import convert_datetime_to_aware_timezone, get_timezone
from models.emails import Email, EmailQuery, EmailStatusChoices


class EmailSerializer(Serializer):
    model = Email
    model_query = EmailQuery

    event_id = fields.Integer(required=True, validate=validate.Range(min=1, error=MessageInvalid.MIN_POSITIVE_VALUE))
    email_subject = fields.Str(required=True, validate=validate.Length(max=Email.MAX_EMAIL_SUBJECT))
    email_content = fields.Str(required=True)

    timestamp = fields.DateTime(
        required=True,
        format=const.EMAIL_TIMESTAMP_FORMAT,
        error_messages={"invalid": MessageInvalid.TIMESTAMP_FORMAT}
    )
    status = fields.Function(lambda obj: obj.status.value if obj.status else obj.status, dump_only=True)

    class Meta:
        fields = (
            "event_id",
            "email_subject",
            "email_content",
            "timestamp",
            "status"
        )

    @validates("event_id")
    def validate_event_id(self, value):
        if EmailQuery.get_by_event_id(value):
            raise ValidationError(MessageInvalid.INVALID_EXIST_DATA.format("Event ID"))

    @validates_schema
    def validates_data(self, data, **kwargs):
        timezone = get_timezone()
        dt_now = datetime.now(tz=timezone)
        dt_now_str = dt_now.strftime(const.EMAIL_TIMESTAMP_FORMAT)
        threshold = settings.EMAIL_TIMESTAMP_THRESHOLD

        timestamp = data["timestamp"]
        dt_input_aware_timezone = convert_datetime_to_aware_timezone(timestamp, timezone)

        delta_dt = (dt_input_aware_timezone - dt_now).total_seconds()
        if delta_dt < threshold * 60:
            raise ValidationError(
                MessageInvalid.TIMESTAMP_THRESHOLD.format(threshold, dt_now_str), field_name="timestamp"
            )

        data['timestamp'] = dt_input_aware_timezone
        return data

    def is_valid(self, payload):
        self.validated_data = self.load(payload)
        self.validated_data["status"] = EmailStatusChoices.PENDING

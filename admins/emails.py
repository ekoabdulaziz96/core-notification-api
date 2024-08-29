from flask_admin.contrib import sqla
from wtforms import validators

from cores.extensions import admin, db
from cores.utils import get_timezone
from models.emails import Email, EmailHistory, UserRecipient


class EmailAdmin(sqla.ModelView):
    page_size = 5
    page_size_options = (5, 10, 15)
    can_set_page_size = True

    action_disallowed_list = ["delete"]
    can_create = False
    can_edit = False
    can_delete = False
    can_view_details = True

    column_list = ["event_id", "email_subject", "email_content", "timestamp", "status"]

    column_formatters = {"timestamp": lambda v, c, m, p: m.timestamp.astimezone(tz=get_timezone())}


class UserRecipientAdmin(sqla.ModelView):
    page_size = 5
    page_size_options = (5, 10, 15)
    can_set_page_size = True

    action_disallowed_list = ["delete"]
    can_view_details = True

    column_list = ["email", "is_active"]
    form_excluded_columns = ["created_at", "updated_at"]

    form_args = {
        "email": {"validators": [validators.Email()]},
    }


class EmailHistoryAdmin(sqla.ModelView):
    page_size = 5
    page_size_options = (5, 10, 15)
    can_set_page_size = True

    action_disallowed_list = ["delete"]
    can_create = False
    can_edit = False
    can_delete = False
    can_view_details = True

    column_list = ["id", "email", "email_recipients", "status", "err_message"]


admin.add_view(EmailAdmin(Email, db.session))
admin.add_view(UserRecipientAdmin(UserRecipient, db.session))
admin.add_view(EmailHistoryAdmin(EmailHistory, db.session))

from flask import Blueprint

from cores.middlewares import middleware
from views import emails as views_emails

bp_emails = Blueprint("emails", __name__)


@bp_emails.route("/save_emails", methods=["POST"], endpoint="save-emails")
def list_create_users():
    return middleware.process(views_emails.ManageEmail, "save")

from flask import Blueprint

from admins import emails  # noqa

bp_admins = Blueprint("admin_bp", "admins")

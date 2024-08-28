from celery import current_app as celery

from models.emails import EmailQuery
from modules.emails import module_email


@celery.task
def task_celery(inp=None):  # pragma: no cover
    print(f"Pong: {inp}")


@celery.task
def task_send_email():
    emails = EmailQuery.get_all_by_current_datetime()
    if len(emails) > 0:
        module_email.process_send_email(emails)
    else:
        print("no email to process")

    return str(emails)

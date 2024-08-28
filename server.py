from cores.app import create_app, create_worker_app, make_celery
from cores.settings import SCHEDULE_TASK_INTERVAL_SEND_EMAIL
from tasks.workers import task_celery, task_send_email

# ----------------------------- init app
app = create_app()
celery = make_celery(create_worker_app())


# ----------------------------- celery-beat set periodic task
@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # sender.add_periodic_task(5, task_celery.s(inp="hola"), name="test-every-5")
    sender.add_periodic_task(
        SCHEDULE_TASK_INTERVAL_SEND_EMAIL,
        task_send_email,
        name=f"task-send-email-every-{SCHEDULE_TASK_INTERVAL_SEND_EMAIL}-second",
    )


# ----------------------------- route index
@app.route("/", methods=["GET"])
def index():
    return "core-notification-api", 200


@app.route("/test-celery", methods=["GET"])
def test_celery():
    task_celery.delay(inp="test-input")
    return "test-celery", 200

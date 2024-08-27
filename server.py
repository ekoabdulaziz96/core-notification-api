from cores.app import create_app, create_worker_app, make_celery

# ----------------------------- init app
app = create_app()
celery = make_celery(create_worker_app())


# ----------------------------- celery-beat set periodic task
@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # import random
    # sender.add_periodic_task(5, workers.task_celery.s(inp=f'scheduled {random.randint(1,1000)}'), name='test-every-5')
    pass


# ----------------------------- route index
@app.route("/", methods=["GET"])
def index():
    print("print_log_core_notif")
    return "backep-api", 200


@app.route("/test-celery", methods=["GET"])
def test_celery():
    print("print_log_core_notif")
    return "test-celery", 200

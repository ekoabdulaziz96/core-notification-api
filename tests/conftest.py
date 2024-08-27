import logging

import pytest
from webtest import TestApp

from cores.app import create_app
from cores.extensions import db as _db


@pytest.fixture(scope="session")
def app():
    """Create application for the tests."""
    _app = create_app("tests.settings")
    _app.logger.setLevel(logging.CRITICAL)
    ctx = _app.test_request_context()
    ctx.push()

    yield _app

    ctx.pop()


@pytest.fixture(scope="session")
def test_app(app):
    """Create Webtest app."""
    return TestApp(app)


@pytest.fixture(scope="session")
def db(app):
    """Create database for the tests."""
    _db.app = app
    with app.app_context():
        _db.create_all()

    _db.session.configure(expire_on_commit=False)

    yield _db

    # Explicitly close DB connection
    _db.session.close()
    _db.drop_all()


@pytest.fixture
def client_test(request, test_app, db, app):
    """Create Client Webtest app."""

    request.cls.test_app = test_app  # using webtest library
    request.cls.client_app = app.test_client()  # using flask test
    request.cls.db = db

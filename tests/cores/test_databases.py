from unittest import skip, TestCase

from sqlalchemy.sql import text

from cores.extensions import db
from server import app


@skip("only check test for real server")
class TestDatabaseSqlConnection(TestCase):   # pragma: no cover
    @classmethod
    def setUpClass(cls):
        """call once a time"""
        super(TestDatabaseSqlConnection, cls).setUpClass()
        # instance app Flask and client
        cls.app = app
        cls.app.debug = True

    def test_success_connection(self):
        conn_status = False
        try:
            db.app = self.app
            with self.app.app_context():
                if db.session.execute(text("SELECT 1")):
                    conn_status = True
        except Exception as err:
            print("database not connect", err)

        self.assertTrue(conn_status)

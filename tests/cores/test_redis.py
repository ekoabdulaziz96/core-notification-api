from time import sleep
from unittest import skip, TestCase

from cores.extensions import cache
from server import app


@skip("only check test for real server")
class TestCacheConnection(TestCase):  # pragma: no cover
    @classmethod
    def setUpClass(cls):
        super(TestCacheConnection, cls).setUpClass()

        # instance app Flask and client
        cls.app = app
        cls.app.debug = True
        cls.client = cls.app.test_client()

    def test_success_cache(self):
        cache.init_app(self.app)

        result = cache.set("name_key", "custom_value", 1)  # key, valvue, timeout in seconds
        self.assertTrue(result)
        self.assertEqual(cache.get("name_key"), "custom_value")

        sleep(1)
        self.assertNotEqual(cache.get("name_key"), "custom_value")

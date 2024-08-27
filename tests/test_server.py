from unittest import TestCase

from pytest import mark


@mark.usefixtures("client_test")
class TestServer(TestCase):
    def setUp(self):
        print("setupp")

    def tearDown(self):
        print("teardown")

    def test_case_1(self):
        print("test 1")

    def test_case_2(self):
        print("test 2")

import unittest
import request


class EasyTests(unittest.TestCase):

    def test_register(self):
        self.assertEqual(request.Request("register user15 password"), "Successful register.")

    def test_delete(self):
        self.assertEqual(request.Request("delete user user15"), "Successful delete.")


class TestCases(unittest.TestCase):

    def test_case_register(self):
        for i in range(15):
            self.assertEqual(request.Request("register games" + str(i) + " password"), "Successful register.")

    def test_case_delete(self):
        for i in range(15):
            self.assertEqual(request.Request("delete user games" + str(i)), "Successful delete.")

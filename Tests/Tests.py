import unittest
import request


class EasyTests(unittest.TestCase):

    def test_register(self):
        self.assertEqual(request.Request("register user15 password"), "Successful register.")

    def test_login(self):
        self.assertEqual(request.Request("login user15 password"), "user15")

    def test_change_password(self):
        self.assertEqual(request.Request("change password user15 password password1"), "Successful changes.")

    def test_update_name(self):
        self.assertEqual(request.Request("update name user15 user17"), "Successful update.")

    def test_update_score(self):
        self.assertEqual(request.Request("update score user17 200 20"), "Successful update.")

    def test_delete(self):
        self.assertEqual(request.Request("delete user user15"), "Successful delete.")




class HardTests(unittest.TestCase):

    def test_register(self):
        for i in range(15):
            self.assertEqual(request.Request("register games" + str(i) + " password"), "Successful register.")

    def test_delete(self):
        for i in range(15):
            self.assertEqual(request.Request("delete user games" + str(i)), "Successful delete.")


class TestCases(unittest.TestCase):

    def test_register_and_delete(self):
        for i in range(15):
            self.assertEqual(request.Request("register games" + str(i) + " password"), "Successful register.")
        for i in range(15):
            self.assertEqual(request.Request("delete user games" + str(i)), "Successfu l delete.")

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
        self.assertEqual(request.Request("delete user user17"), "Successful delete.")

    def test_add_map_rating(self):
        self.assertEqual(request.Request("add map1 3 user17"), "Successful added")

    def test_change_rating(self):
        self.assertEqual(request.Request("change rating map1 4 user17"), "Successful added")

    def test_delete_rating_m(self):
        self.assertEqual(request.Request("delete rating-m map1"), "Successful delete")

    def test_delete_rating_u(self):
        self.assertEqual(request.Request("delete rating-u user17"), "Successful delete.")

class HardTests(unittest.TestCase):

    def test_register(self):
        for i in range(15):
            self.assertEqual(request.Request("register gamer" + str(i) + " password" + str(i)), "Successful register.")

    def test_add_map_rating(self):
        for i in range(15):
            self.assertEqual(request.Request("add map1 4 gamer" + str(i)), "Successful added")

    def test_change_rating(self):
        for i in range(15):
            self.assertEqual(request.Request("change rating map1 1 gamer" + str(i)), "Successful added")

    def test_delete_rating_u(self):
        for i in range(15):
            self.assertEqual(request.Request("delete rating-u gamer" + str(i)), "Successful delete.")

    def test_add_map_rating2(self):
        for i in range(15):
            self.assertEqual(request.Request("add map" + str(i) + " 4 gamer17"), "Successful added")

    def test_delete_rating_m(self):
        for i in range(15):
            self.assertEqual(request.Request("delete rating-u map" + str(i)), "Successful delete.")


    def test_login(self):
        for i in range(15):
            self.assertEqual(request.Request("login gamer" + str(i) + " password" + str(i)), "gamer" + str(i))

    def test_change_password(self):
        for i in range(15):
            self.assertEqual(request.Request("change password gamer" + str(i) + " password" + str(i) + " password"), "Successful changes.")

    def test_update_name(self):
        for i in range(15):
            self.assertEqual(request.Request("update name gamer" + str(i) + " gamer" + str(i+10)), "Successful update.")

    def test_update_score(self):
        for i in range(15):
            self.assertEqual(request.Request("update score gamer" + str(i+10) + " " + str(i*100) + " " + str(i*10)), "Successful update.")

    def test_delete(self):
        for i in range(15):
            self.assertEqual(request.Request("delete user gamer" + str(i+10)), "Successful delete.")




class TestCases(unittest.TestCase):

    def test_register_and_delete(self):
        for i in range(15):
            self.assertEqual(request.Request("register gamer" + str(i) + " password"), "Successful register.")
        for i in range(15):
            self.assertEqual(request.Request("delete user gamer" + str(i)), "Successful delete.")

    def test_register_login_update_name_login_and_delete(self):
        for i in range(15):
            self.assertEqual(request.Request("register gamer" + str(i) + " password"), "Successful register.")
        for i in range(15):
            self.assertEqual(request.Request("login gamer" + str(i) + " password"), "gamer" + str(i))
        for i in range(15):
            self.assertEqual(request.Request("update name gamer" + str(i) + " gamer" + str(i+20)), "Successful update.")
        for i in range(15):
            self.assertEqual(request.Request("login gamer" + str(i+20) + " password"), "gamer" + str(i+20))
        for i in range(15):
            self.assertEqual(request.Request("delete user gamer" + str(i+20)), "Successful delete.")

    def test_register_double_score_update_and_delete(self):
        for i in range(15):
            self.assertEqual(request.Request("register gamer" + str(i) + " password"), "Successful register.")
        for i in range(15):
            self.assertEqual(request.Request("update score gamer" + str(i) + " " + str(i*100) + " " + str(i*10)), "Successful update.")
        for i in range(15):
            self.assertEqual(request.Request("update score gamer" + str(i) + " " + str(i*10) + " " + str(i*100)), "Successful update.")
        for i in range(15):
            self.assertEqual(request.Request("delete user gamer" + str(i)), "Successful delete.")

    def test_register_add_ratings_for_ome_map_change_ratings_delete(self):
        for i in range(15):
            self.assertEqual(request.Request("register gamer" + str(i) + " password" + str(i)), "Successful register.")
        for i in range(15):
            self.assertEqual(request.Request("add map1 5 gamer" + str(i)), "Successful added")
        for i in range(15):
            self.assertEqual(request.Request("change rating map1 1 gamer" + str(i)), "Successful added")
        for i in range(15):
            self.assertEqual(request.Request("delete rating-u gamer" + str(i)), "Successful delete.")
        for i in range(15):
            self.assertEqual(request.Request("delete user gamer" + str(i)), "Successful delete.")

    def test_register_add_ratings_for_different_maps_change_ratings_delete(self):
        for i in range(15):
            self.assertEqual(request.Request("register gamer" + str(i) + " password" + str(i)), "Successful register.")
        for i in range(15):
            self.assertEqual(request.Request("add map" + str(i) + " 4 gamer17"), "Successful added")
        for i in range(15):
            self.assertEqual(request.Request("change rating map" + str(i) + " 1 gamer17"), "Successful added")
        for i in range(15):
            self.assertEqual(request.Request("delete rating-u map" + str(i)), "Successful delete.")
        for i in range(15):
            self.assertEqual(request.Request("delete user gamer" + str(i)), "Successful delete.")


    #много комментов к одной карте
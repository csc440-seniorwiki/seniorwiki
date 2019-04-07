import unittest

from pathlib import Path
import os
import re

from wiki.web import create_app
from wiki.web import current_users
from wiki.web import current_group_manager
from wiki.web.roles import wiki_permissions

admin = {'username': 'admin', 'password': "password"}
user = {'username': 'sam', 'password': "1234"}
user_invalid_credentials = {'username': 'sam', 'password': "incorrect_password"}
hashed_password_user = {'username': 'wasd', 'password': "wasd"}
hashed_password_user_invalid_credentials = {'username': 'wasd', 'password': "incorrect_password"}


def login_to_website(user, client):
    rv = client.get('/user/login/')
    m = re.search(b'<input id="csrf_token" name="csrf_token" type="hidden" value="(.*)">', rv.data)
    return client.post('/user/login/', data=dict(
        name=user['username'],
        password=user['password'],
        csrf_token=m.group(1).decode("utf-8")
    ), follow_redirects=True)


def setup_testing_directory(directory):
    os.mkdir(directory + "/testing/")
    f = open("./testing/users.json", "w+")
    f.write('{  "admin": {    "active": true,    "authentication_method": "cleartext",    "password": "password",    "authenticated": false,    "roles": [],    "groups": [      "administrators"    ]  },  "name": {    "active": true,    "authentication_method": "cleartext",    "password": "1234",    "authenticated": true,    "roles": [      "wiki_edit",      "wiki_delete",      "wiki_rename_page",      "wiki_create_page",      "wiki_edit_protected",      "wiki_delete_user",      "wiki_edit_user",      "wiki_edit_group",      "wiki_delete_group",      "wiki_create_group"    ],    "groups": []  },  "sam": {    "active": true,    "authentication_method": "cleartext",    "password": "1234",    "authenticated": false,    "roles": []  },  "aname": {    "active": true,    "authentication_method": "cleartext",    "authenticated": false,    "password": "12341234",    "roles": []  },  "wasd": {    "active": true,    "authentication_method": "hash",    "authenticated": false,    "roles": [],    "groups": [],    "hash": "$2a$12$pNoxxzvdSchc86PBxPiiS.ifMZA60lXfVc5KGH2IBp6tTKvltR1ii"  }}')
    f.close()
    f = open("./testing/groups.json", "w+")
    f.write('{"administrators": {"roles": ["wiki_edit","wiki_delete","wiki_rename_page","wiki_create_page","wiki_edit_protected","wiki_delete_user","wiki_edit_user","wiki_edit_group","wiki_delete_group","wiki_create_group"]}}')
    f.close()


def teardown_testing_directory(directroy):
    os.remove("./testing/users.json")
    os.remove("./testing/groups.json")
    os.rmdir(os.getcwd() + "/testing/")


class PermissionsTest(unittest.TestCase):

    def setUp(cls):
        setup_testing_directory(os.getcwd())
        app = create_app(Path(os.getcwd()).parent.parent)
        app.config['USER_DIR'] = os.getcwd() + "/testing/"
        cls.app = app
        cls.client = app.test_client()

    def tearDown(self):
        teardown_testing_directory(os.getcwd())

    def test_login_page_loads_anonymously(self):
        r = self.client.get('/user/login/')
        self.assertEqual(200, r.status_code)

    def test_login_admin_account(self):
        r = login_to_website(admin, self.client)
        self.assertEqual(200, r.status_code)
        self.assertIn("Login successful", str(r.data))

    def test_logout(self):
        with self.client:
            login_to_website(admin, self.client)
            r = self.client.get("/user/logout/", follow_redirects=True)
            self.assertEqual(200, r.status_code)
            self.assertIn("Logout successful", str(r.data))

    def test_admin_account_can_view_index(self):
        with self.client:
            login_to_website(admin, self.client)
            r = self.client.get('/index/')
            self.assertEqual(200, r.status_code)

    def test_admin_can_load_change_user_permissions_page(self):
        login_to_website(admin, self.client)
        r = self.client.get('/user/admin/')
        self.assertEqual(200, r.status_code)

    def test_user_cannot_load_change_user_permissions_page(self):
        with self.client:
            login_to_website(user, self.client)
            r = self.client.get('/user/admin/')
            self.assertEqual(401, r.status_code)

    def test_admin_can_load_edit_page(self):
        login_to_website(admin, self.client)
        r = self.client.get('/edit/hi/')
        self.assertEqual(200, r.status_code)

    def test_user_cannot_load_edit_page(self):
        with self.client:
            login_to_website(user, self.client)
            r = self.client.get('/edit/hi/')
            self.assertEqual(401, r.status_code)

    def test_user_can_load_homepage(self):
        with self.client:
            login_to_website(user, self.client)
            r = self.client.get('/index/')
            self.assertEqual(200, r.status_code)

    def test_admin_can_load_edit_page(self):
        login_to_website(admin, self.client)
        r = self.client.get('/edit/hi/')
        self.assertEqual(200, r.status_code)

    def test_user_cannot_load_edit_page(self):
        login_to_website(user, self.client)
        r = self.client.get('/edit/hi/')
        self.assertEqual(401, r.status_code)

    def test_admin_account_has_all_permissions(self):
        with self.client:
            r = login_to_website(admin, self.client)
            for i in range(0, len(wiki_permissions)):
                self.assertEqual(True, wiki_permissions[i].can())

    def test_user_account_has_no_permissions(self):
        with self.client:
            r = login_to_website(user, self.client)
            for i in range(0, len(wiki_permissions)):
                self.assertEqual(False, wiki_permissions[i].can())


class FunctionTest(unittest.TestCase):

    def setUp(cls):
        setup_testing_directory(os.getcwd())
        app = create_app(Path(os.getcwd()).parent.parent)
        app.config['USER_DIR'] = os.getcwd() + "/testing/"
        cls.app = app
        cls.client = app.test_client()

    def tearDown(self):
        teardown_testing_directory(os.getcwd())

    def test_login_admin_account(self):
        r = login_to_website(admin, self.client)
        self.assertEqual(200, r.status_code)
        self.assertIn("Login successful", str(r.data))

    def test_login_hashed_password(self):
        r = login_to_website(hashed_password_user, self.client)
        self.assertEqual(200, r.status_code)
        self.assertIn("Login successful", str(r.data))

    def test_login_user_account_fails_with_invalid_credentials(self):
        r = login_to_website(user_invalid_credentials, self.client)
        self.assertEqual(200, r.status_code)
        self.assertNotIn("Login successful", str(r.data))

    def test_login_hashed_password_fails_with_invalid_credentials(self):
        r = login_to_website(hashed_password_user_invalid_credentials, self.client)
        self.assertEqual(200, r.status_code)
        self.assertNotIn("Login successful", str(r.data))

    def test_register_user(self):
        username = "test"
        password = "test"
        with self.client:
            rv = self.client.get('/user/register/')
            m = re.search(b'<input id="csrf_token" name="csrf_token" type="hidden" value="(.*)">', rv.data)
            self.client.post('/user/register/', data=dict(
                name=username,
                password=password,
                csrf_token=m.group(1).decode("utf-8")
            ), follow_redirects=True)
            r = login_to_website({'username': username, 'password': password}, self.client)
            self.assertEqual(200, r.status_code)
            self.assertIn("Login successful", str(r.data))

    def test_delete_user(self):
        with self.client:
            login_to_website(admin, self.client)
            self.client.get("/user/delete/sam/")
            self.client.get("/user/logout/", follow_redirects=True)
            r = login_to_website(user, self.client)
            self.assertEqual(200, r.status_code)
            self.assertIn("Errors occured verifying your input. Please check the marked fields below.", str(r.data))

    def test_set_user_roles(self):
        with self.client:
            login_to_website(admin, self.client)
            rv = self.client.get('/user/sam/')
            m = re.search(b'<input id="csrf_token" name="csrf_token" type="hidden" value="(.*)">', rv.data)
            self.client.post('/user/sam/', data=dict(
                roles="wiki_edit",
                csrf_token=m.group(1).decode("utf-8")
            ), follow_redirects=True)
            self.client.get("/user/logout/", follow_redirects=True)
            login_to_website(user, self.client)
            self.assertEqual(True, wiki_permissions[0].can())

    def test_set_user_groups(self):
        with self.client:
            login_to_website(admin, self.client)
            rv = self.client.get('/user/sam/')
            m = re.search(b'<input id="csrf_token" name="csrf_token" type="hidden" value="(.*)">', rv.data)
            self.client.post('/user/sam/', data=dict(
                groups="administrators",
                csrf_token=m.group(1).decode("utf-8")
            ), follow_redirects=True)
            self.client.get("/user/logout/", follow_redirects=True)
            login_to_website(user, self.client)
            self.assertEqual(True, wiki_permissions[0].can())

    def test_create_group(self):
        with self.client:
            login_to_website(admin, self.client)
            rv = self.client.get('/user/sam/')
            m = re.search(b'<input id="csrf_token" name="csrf_token" type="hidden" value="(.*)">', rv.data)
            self.client.post('/group/create/', data=dict(
                name="test_group",
                csrf_token=m.group(1).decode("utf-8")
            ), follow_redirects=True)
            self.assertNotEqual(None, current_group_manager.get_group('test_group'))

    def test_delete_group(self):
        with self.client:
            login_to_website(admin, self.client)
            self.client.get("/group/delete/administrators/")
            self.assertEqual(None, current_group_manager.get_group('Administrators'))

if __name__ == '__main__':
    unittest.main()

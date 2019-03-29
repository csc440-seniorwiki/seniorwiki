import unittest

from pathlib import Path

import os
import re

from wiki.web import create_app


def login_to_website(user, client):
    rv = client.get('/user/login/')
    m = re.search(b'<input id="csrf_token" name="csrf_token" type="hidden" value="(.*)">', rv.data)
    return client.post('/user/login/', data=dict(
        name=user['username'],
        password=user['password'],
        csrf_token=m.group(1).decode("utf-8")
    ), follow_redirects=True)


class PermissionsTest(unittest.TestCase):

    admin = {'username': 'admin', 'password': "password"}
    user = {'username': 'sam', 'password': "1234"}

    @classmethod
    def setUpClass(cls):
        app = create_app(Path(os.getcwd()).parent.parent)
        cls.app = app
        cls.client = app.test_client()

    def test_login_page_loads_anonymously(self):
        r = self.client.get('/user/login/')
        self.assertEqual(200, r.status_code)

    def test_login_admin_account(self):
        r = login_to_website(self.admin, self.client)
        self.assertEqual(200, r.status_code)
        self.assertIn("Login successful", str(r.data))

    def test_logout(self):
        r = self.client.get("/user/logout/", follow_redirects=True)
        self.assertEqual(200, r.status_code)
        self.assertIn("Logout successful", str(r.data))

    def test_admin_account_can_view_index(self):
        login_to_website(self.admin, self.client)
        r = self.client.get('/index/')
        self.assertEqual(200, r.status_code)

    def test_admin_can_load_change_user_permissions_page(self):
        login_to_website(self.admin, self.client)
        r = self.client.get('/user/admin/')
        self.assertEqual(r.status_code, 200)

    def test_user_cannot_load_change_user_permissions_page(self):
        login_to_website(self.user, self.client)
        r = self.client.get('/user/admin/')
        self.assertEqual(r.status_code, 401)

    def test_admin_can_load_edit_page(self):
        login_to_website(self.admin, self.client)
        r = self.client.get('/edit/hi/')
        self.assertEqual(r.status_code, 200)

    def test_user_cannot_load_edit_page(self):
        login_to_website(self.user, self.client)
        r = self.client.get('/edit/hi/')
        self.assertEqual(r.status_code, 401)

    def test_admin_can_load_edit_page(self):
        login_to_website(self.admin, self.client)
        r = self.client.get('/edit/hi/')
        self.assertEqual(r.status_code, 200)

    def test_user_cannot_load_edit_page(self):
        login_to_website(self.user, self.client)
        r = self.client.get('/edit/hi/')
        self.assertEqual(r.status_code, 401)


if __name__ == '__main__':
    unittest.main()

import unittest
import os
import re
import hashlib
from pathlib import Path
from wiki.web import create_app


admin = {'username': 'admin', 'password': "password"}


def login_to_website(user, client):
    rv = client.get('/user/login/')
    m = re.search(b'<input id="csrf_token" name="csrf_token" type="hidden" value="(.*)">', rv.data)
    return client.post('/user/login/', data=dict(
        name=user['username'],
        password=user['password'],
        csrf_token=m.group(1).decode("utf-8")
    ), follow_redirects=True)


class ConversionTests(unittest.TestCase):

    def setUp(self):
        app = create_app(Path(os.getcwd()).parent.parent)
        self.app = app
        self.client = app.test_client()

    def test_single_page_pdf(self):
        with self.client:
            login_to_website(admin, self.client)
            actual_response = self.client.get('/pdf/pdftest1/pdftest1/')
        assert actual_response.mimetype == "application/pdf"
        actual = actual_response.data
        assert actual.startswith(b'%PDF')
        assert b'PDFTest1' in actual
        assert b'CreationDate' in actual
        assert b'localhost' in actual
        actual = re.sub(rb'localhost', b'127.0.0.1:5000', actual, flags=re.MULTILINE)
        actual = re.sub(rb'.*CreationDate.*\n?', b'', actual, flags=re.MULTILINE)
        assert b'PDFTest1' in actual
        assert b'CreationDate' not in actual
        assert b'localhost' not in actual
        f = open("single_page_test.pdf", "rb")
        expected = f.read()
        f.close()
        self.assertEqual(hashlib.md5(expected).hexdigest(), hashlib.md5(actual).hexdigest())

    def test_multiple_page_pdf(self):
        with self.client:
            login_to_website(admin, self.client)
            actual_response = self.client.post('/selectpdf/', data=dict(page=['PDFTest1/PDFTest1', 'PDFTest2/PDFTest2']), follow_redirects=True)
        assert actual_response.mimetype == "application/pdf"
        actual = actual_response.data
        assert actual.startswith(b'%PDF')
        assert b'PDFTest1' in actual
        assert b'PDFTest2' in actual
        assert b'CreationDate' in actual
        assert b'localhost' in actual
        actual = re.sub(rb'localhost', b'127.0.0.1:5000', actual, flags=re.MULTILINE)
        actual = re.sub(rb'.*CreationDate.*\n?', b'', actual, flags=re.MULTILINE)
        assert b'PDFTest1' in actual
        assert b'PDFTest2' in actual
        assert b'CreationDate' not in actual
        assert b'localhost' not in actual
        f = open("multiple_page_test.pdf", "rb")
        expected = f.read()
        f.close()
        self.assertEqual(hashlib.md5(expected).hexdigest(), hashlib.md5(actual).hexdigest())


if __name__ == '__main__':
    unittest.main()

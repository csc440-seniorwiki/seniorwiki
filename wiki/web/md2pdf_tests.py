import unittest
import os
import re
import hashlib
from weasyprint import HTML
from pathlib import Path
from wiki.web import create_app
from wiki.web.md2pdf import md2pdf_single_page
from wiki.web.md2pdf import md2pdf_multiple_page
from wiki.web.md2pdf import md2pdf_full_wiki


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
            response = self.client.get('/pdf/pdftest1/')#, follow_redirects=True)
            assert response.mimetype == "application/pdf"
            pdf = response.data
            assert pdf.startswith(b'%PDF')
            assert b'AsciiDots' in pdf
        with self.app.test_request_context():
            received = md2pdf_single_page('pdftest1', 'pdf_page.html')
        assert received.mimetype == "application/pdf"
        assert 'Content-Disposition' not in response.headers
        assert b'AsciiDots' in received.data
        assert b'CreationDate' in pdf
        pdf = re.sub(rb'.*CreationDate.*\n?', b'', pdf, flags=re.MULTILINE)
        received.data = re.sub(rb'.*CreationDate.*\n?', b'', received.data, flags=re.MULTILINE)
        assert b'CreationDate' not in pdf
        assert b'AsciiDots' in pdf
        self.assertEqual(hashlib.md5(pdf).hexdigest(), hashlib.md5(received.data).hexdigest())


if __name__ == '__main__':
    unittest.main()

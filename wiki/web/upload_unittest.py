import unittest
import os
import io
from wiki.web import routes
from flask import Flask

app = Flask(__name__)
app.register_blueprint(routes.bp)


class UploadTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pic/')

        if os.path.exists(os.path.join(path, "test_img.jpg")):
            os.remove(os.path.join(path, "test_img.jpg"))

    def test_upload(self):
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pic/')
        r = app.test_client(self)
        r.post('/upload/', data=dict(file=(io.BytesIO(b"test"), 'test_img.jpg'),), follow_redirects=True)

        self.assertTrue(os.path.exists(os.path.join(path, "test_img.jpg")), "File not found!")


if __name__ == '__main__':
    unittest.main()

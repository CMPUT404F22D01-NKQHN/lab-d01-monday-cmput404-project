
from unittest.mock import patch
from posts.tests.utils import *

class UITestCase(TestCase, SnapshotTestCase):
    def setUp(self):
        self.author = create_author("test","test","test","test", "123")
    def test_home_unauth(self):
        response = self.client.get("/")
        # Should redirect to login
        self.assertEqual(response.status_code, 302)
    def test_home(self):
        self.client.force_login(self.author)
        # Mock all requests to use client
        with patch("requests.get") as mock_get:
            mock_get.side_effect = lambda url: self.client.get(url)
            response = self.client.get("/")
            self.assertEqual(response.status_code, 200)
            self.assertMatchSnapshot(response.content.decode("utf-8"))
    
    
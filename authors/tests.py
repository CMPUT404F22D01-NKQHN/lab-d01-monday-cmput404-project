from django.test import TestCase
from .models import Author, AuthorManager
from posts.tests.utils import create_author


class AuthorTestCase(TestCase):
    def setUp(self):
        self.test1 = create_author("test", "test1", "test1", "test1")
        self.test2 = create_author("test2", "test2", "test2", "test2")
        self.test_server = Author.objects.create(
            display_name="server",
            email="server",
            password="server",
            username="server",
            is_another_server=True,
        )

    def test_duplicate_fail(self):
        try:
            test1 = Author.objects.create(
                display_name="test", email="test1", password="test1", username="test1"
            )
            test2 = Author.objects.create(
                display_name="test", email="test1", password="test1", username="test1"
            )
        except:
            pass
        else:
            self.fail("Duplicate author created")

    def test_get_all(self):
        self.client.force_login(self.test1)
        res = self.client.get("/authors/")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.data), 2)
        self.assertEqual(res.data["items"][0]["display_name"], "test")

    def test_user_manager(self):
        test1 = Author.objects.create_user(
            display_name="test", email="test1", password="test1", username="normal"
        )
        test2 = Author.objects.create_superuser(
            display_name="test2", email="test2", password="test2", username="super"
        )
        self.assertTrue(not test1.is_staff)
        self.assertTrue(test2.is_staff)

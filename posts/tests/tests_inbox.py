from posts.serializers import ReadPostSerializer
from .utils import *


class InboxTestCase(TestCase):
    def setUp(self) -> None:
        self.author = create_author("test", "test", "test", "test")
        self.author2 = create_author("test2", "test2", "test2", "test2")

        self.author.followers.add(self.author2)
        self.author.save()

    def test_add_post(self):
        self.client.force_login(self.author)
        response = self.client.post(
            "/authors/" + str(int(self.author.id)) + "/posts",
            POST_DATA,
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.client.force_login(self.author2)
        response = self.client.get("/authors/" + str(int(self.author2.id)) + "/inbox")
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(len(response_data["items"]), 1)
        self.assertEqual(response_data["items"][0]["type"], "post")

    def test_add_comment(self):
        post = create_post(self.author)
        self.client.force_login(self.author2)
        response = self.client.post(
            "/authors/"
            + str(int(self.author.id))
            + "/posts/"
            + str(int(post.id))
            + "/comments",
            {"content": "test comment"},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.client.force_login(self.author)
        response = self.client.get("/authors/" + str(int(self.author.id)) + "/inbox")
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(len(response_data["items"]), 1)
        self.assertEqual(response_data["items"][0]["type"], "comment")

    def test_add_like(self):
        post = create_post(self.author)
        self.client.force_login(self.author2)
        response = self.client.post(
            "/authors/"
            + str(int(self.author.id))
            + "/posts/"
            + str(int(post.id))
            + "/likes"
        )
        self.assertEqual(response.status_code, 200)
        self.client.force_login(self.author)
        response = self.client.get("/authors/" + str(int(self.author.id)) + "/inbox")
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(len(response_data["items"]), 1)
        self.assertEqual(response_data["items"][0]["type"], "like")

    def test_send_to_inbox(self):
        self.client.force_login(self.author2)
        # send a post to the inbox
        post = create_post(self.author)

        self.client.post(
            "/authors/" + str(int(self.author.id)) + "/inbox",
            json.dumps({"item": ReadPostSerializer(post).data}),
            content_type="application/json",
        )
        self.client.force_login(self.author)
        response = self.client.get("/authors/" + str(int(self.author.id)) + "/inbox")
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(len(response_data["items"]), 1)

    def test_clear_inbox(self):
        self.client.force_login(self.author2)
        # send a post to the inbox
        for i in range(10):
            post = create_post(self.author)
            self.client.post(
                "/authors/" + str(int(self.author.id)) + "/inbox",
                json.dumps(
                    {
                        "item": ReadPostSerializer(post).data,
                    }
                ),
                content_type="application/json",
            )
        self.client.force_login(self.author)
        response = self.client.get(
            "/authors/" + str(int(self.author.id)) + "/inbox?page=1&size=10"
        )
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(len(response_data["items"]), 10)
        response = self.client.delete("/authors/" + str(int(self.author.id)) + "/inbox")
        self.assertEqual(response.status_code, 200)
        response = self.client.get("/authors/" + str(int(self.author.id)) + "/inbox")

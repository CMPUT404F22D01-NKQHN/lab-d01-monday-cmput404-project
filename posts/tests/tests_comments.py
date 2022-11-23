from .utils import *


class CommentsTestCase(TestCase):
    def test_add_comment_to_post(self):
        author = create_author("test", "test", "test", "test")
        post = create_post(author)
        comment_data = {
            "comment": "This is a comment",
        }
        self.client.force_login(author)
        response = self.client.post(
            "/authors/"
            + author.id
            + "/posts/"
            + post.id
            + "/comments",
            comment_data,
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(response_data["post_id"], str(post.id))
        response = self.client.get(
            "/authors/"
            + author.id
            + "/posts/"
            + post.id
            + "/comments",
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(len(response_data["comments"]), 1)
        self.assertEqual(response_data["comments"][0]["comment"], "This is a comment")


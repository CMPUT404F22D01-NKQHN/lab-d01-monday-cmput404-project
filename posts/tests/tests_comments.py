from .utils import *


class CommentsTestCase(TestCase):
    def test_add_comment_to_post(self):
        author = create_author("test", "test", "test", "test")
        post = create_post(author)
        comment_data = {
            "content": "This is a comment",
        }
        self.client.force_login(author)
        response = self.client.post(
            "/authors/"
            + str(int(author.id))
            + "/posts/"
            + str(int(post.id))
            + "/comments",
            comment_data,
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(response_data["post_id"], str(post.id))
        response = self.client.get(
            "/authors/"
            + str(int(author.id))
            + "/posts/"
            + str(int(post.id))
            + "/comments",
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(len(response_data), 1)
        self.assertEqual(response_data[0]["content"], "This is a comment")

    def test_reply_to_comment(self):
        # TODO: See if we want replies to comments
        author = create_author("test", "test", "test", "test")
        post = create_post(author)
        comment_data = {
            "content": "This is a comment",
        }
        comment = CreateCommentSerializer().create(comment_data, author, post)
        reply_data = {
            "content": "This is a reply",
        }
        reply = CreateCommentSerializer().create(reply_data, author, post, comment.id)
        self.assertEqual(reply.reply_to, comment.id)
        self.assertTrue(reply in comment.replies.all())

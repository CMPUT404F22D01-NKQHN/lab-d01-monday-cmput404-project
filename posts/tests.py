import base64
import json
from django.test import TestCase
from authors.models import Author

from posts.models import Inbox
from posts.serializers import (
    CreateCommentSerializer,
    CreateLikeSerializer,
    CreatePostSerializer,
    ReadCommentSerializer,
    ReadLikeSerializer,
    ReadPostSerializer,
    ReadInboxSerializer,
    AddInboxItemSerializer,
    UpdatePostSerializer,
)


from django.test import TestCase
from django.test import TestCase


def create_author(display_name, email, password, username):
    return Author.objects.create(
        display_name=display_name,
        email=email,
        password=password,
        username=username,
    )


POST_DATA = {
    "title": "title",
    "source": "source",
    "origin": "origin",
    "description": "description",
    "unlisted": False,
    "visibility": "PUBLIC",
    "contentType": "text/plain",
    "content": "content",
}

POST_DATA_2 = {
    "title": "title",
    "source": "source",
    "origin": "origin",
    "description": "description",
    "unlisted": False,
    "visibility": "FRIENDS",
    "contentType": "text/plain",
    "content": "content",
}


def create_post(author, post_data=POST_DATA):
    return CreatePostSerializer().create(
        post_data.copy(),
        author.id,
    )


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


class PostTestCase(TestCase):
    def test_create_post(self):
        author = create_author("test", "test", "test", "test")
        self.client.force_login(author)
        response = self.client.post(
            "/authors/" + str(int(author.id)) + "/posts",
            POST_DATA,
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)

    def test_create_post_unauthorized(self):
        author = create_author("test", "test", "test", "test")
        author2 = create_author("test2", "test2", "test2", "test2")
        self.client.force_login(author2)
        response = self.client.post(
            "/authors/" + str(int(author.id)) + "/posts",
            POST_DATA,
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 403)

    def test_get_post(self):
        author = create_author("test", "test", "test", "test")
        post = create_post(author)
        response = self.client.get(
            "/authors/" + str(int(author.id)) + "/posts/" + str(int(post.id))
        )
        self.assertEqual(response.status_code, 200)

    def test_get_post_dne(self):
        author = create_author("test", "test", "test", "test")
        response = self.client.get(
            "/authors/" + str(int(author.id)) + "/posts/" + str(int(1))
        )
        self.assertEqual(response.status_code, 404)

    def test_get_post_unauthorized(self):
        author = create_author("test", "test", "test", "test")
        post = create_post(author, POST_DATA_2)
        author2 = create_author("test2", "test2", "test2", "test2")
        self.client.force_login(author2)
        response = self.client.get(
            "/authors/" + str(int(author.id)) + "/posts/" + str(int(post.id))
        )
        self.assertEqual(response.status_code, 403)

    def test_update_post(self):
        author = create_author("test", "test", "test", "test")
        post = create_post(author)
        self.client.force_login(author)
        update_data = {
            "title": "new title",
            "source": "new source",
            "origin": "new origin",
            "description": "new description",
        }
        response = self.client.put(
            "/authors/" + str(int(author.id)) + "/posts/" + str(int(post.id)),
            update_data,
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(response_data["title"], "new title")

    def test_update_post_unauthorized(self):
        author = create_author("test", "test", "test", "test")
        post = create_post(author)
        author2 = create_author("test2", "test2", "test2", "test2")
        self.client.force_login(author2)
        update_data = {
            "title": "new title",
            "source": "new source",
            "origin": "new origin",
            "description": "new description",
        }
        response = self.client.put(
            "/authors/" + str(int(author.id)) + "/posts/" + str(int(post.id)),
            update_data,
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 403)

    def test_delete_post(self):
        author = create_author("test", "test", "test", "test")
        post = create_post(author)
        self.client.force_login(author)
        response = self.client.delete(
            "/authors/" + str(int(author.id)) + "/posts/" + str(int(post.id))
        )
        self.assertEqual(response.status_code, 204)

    def test_delete_post_unauthorized(self):
        author = create_author("test", "test", "test", "test")
        post = create_post(author)
        author2 = create_author("test2", "test2", "test2", "test2")
        self.client.force_login(author2)
        response = self.client.delete(
            "/authors/" + str(int(author.id)) + "/posts/" + str(int(post.id))
        )
        self.assertEqual(response.status_code, 403)

    def test_get_posts_by_author_follower(self):
        author = create_author("test", "test", "test", "test")
        post = create_post(author)
        post2 = create_post(author, POST_DATA_2)
        author2 = create_author("test2", "test2", "test2", "test2")
        author.followers.add(author2)
        author.save()

        self.client.force_login(author2)
        response = self.client.get("/authors/" + str(int(author.id)) + "/posts")
        self.assertEqual(response.status_code, 200)
        response_data = response.json()

        self.assertEqual(len(response_data["items"]), 2)

    def test_get_posts_by_author_public(self):
        author = create_author("test", "test", "test", "test")
        create_post(author)
        create_post(author, POST_DATA_2)
        author2 = create_author("test2", "test2", "test2", "test2")
        self.client.force_login(author2)
        response = self.client.get("/authors/" + str(int(author.id)) + "/posts")
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(len(response_data["items"]), 1)

    def test_get_posts_by_author_dne(self):
        author = create_author("test", "test", "test", "test")
        self.client.force_login(author)
        response = self.client.get("/authors/" + str(int(1)) + "/posts")
        self.assertEqual(response.status_code, 404)

    def test_create_image_post(self):
        author = create_author("test", "test", "test", "test")
        self.client.force_login(author)
        # open posts/test_image/good.png
        image = open("posts/test_image/good.png", "rb")
        base64_image = base64.b64encode(image.read())
        image.close()
        post_data = POST_DATA.copy()
        post_data["contentType"] = "image/png;base64"
        post_data["content"] = base64_image.decode("utf-8")
        response = self.client.post(
            "/authors/" + str(int(author.id)) + "/posts",
            post_data,
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(response_data["contentType"], "image/png;base64")
        self.assertEqual(response_data["content"], base64_image.decode("utf-8"))
        # Get the post and check the image
        response = self.client.get(response_data["id"])
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(response_data["content"], base64_image.decode("utf-8"))


class LikeTestCase(TestCase):
    def test_like_post(self):
        author = create_author("test", "test", "test", "test")
        author2 = create_author("test2", "test2", "test2", "test2")
        post = create_post(author)
        self.client.force_login(author2)
        response = self.client.post(
            "/authors/" + str(int(author.id)) + "/posts/" + str(int(post.id)) + "/likes"
        )
        self.assertEqual(response.status_code, 200)

    def test_like_comment(self):
        author = create_author("test", "test", "test", "test")
        author2 = create_author("test2", "test2", "test2", "test2")
        post = create_post(author)
        self.client.force_login(author2)
        res = self.client.post(
            "/authors/"
            + str(int(author.id))
            + "/posts/"
            + str(int(post.id))
            + "/comments",
            {"content": "test comment"},
            content_type="application/json",
        )
        comment_id = res.json()["id"]
        self.client.force_login(author)
        response = self.client.post(comment_id + "/likes")
        self.assertEqual(response.status_code, 200)


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
            json.dumps(
                {
                    "item_type": "post",
                    "item_id": str(int(post.id)),
                }
            ),
            content_type="application/json",
        )
        self.client.force_login(self.author)
        response = self.client.get("/authors/" + str(int(self.author.id)) + "/inbox")
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(len(response_data["items"]), 1)

from django.test import TestCase
from authors.models import Author

from posts.models import Comment, Inbox, Post
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
from django.test import RequestFactory, TestCase

import posts.views as views


def create_author(display_name, email, password, username):
    return Author.objects.create(
        display_name=display_name,
        email=email,
        password=password,
        username=username,
    )


def create_post(author):
    return CreatePostSerializer().create(
        {
            "title": "title",
            "source": "source",
            "origin": "origin",
            "description": "description",
            "unlisted": False,
            "visibility": "PUBLIC",
            "contentType": "text/plain",
            "content": "content",
        },
        author.id,
    )


class CommentsTestCase(TestCase):
    def test_add_comment_to_post(self):
        author = create_author("test", "test", "test", "test")
        post = create_post(author)
        comment_data = {
            "content": "This is a comment",
        }
        comment = CreateCommentSerializer().create(comment_data, author, post)
        self.assertEqual(comment.post_id, post.id)
        self.assertTrue(comment in post.comments.all())

    def test_reply_to_comment(self):
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
        post = create_post(author)
        self.assertEqual(post.author, author)
    def test_update_post(self):
        author = create_author("test", "test", "test", "test")
        post = create_post(author)
        UpdatePostSerializer(post).update(
            post,
            {
                "title": "newtitle1",
                "source": "source",
            })
        self.assertEqual(post.title, "newtitle1")


class LikeTestCase(TestCase):
    def test_like_post(self):
        author = create_author("test", "test", "test", "test")
        author2 = create_author("test2", "test2", "test2", "test2")
        post = create_post(author)
        like = CreateLikeSerializer().create(
            sender=author2, liked_id=post.id, is_comment=False, accepter=author
        )
        self.assertEqual(like.liked_id, post.id)
        self.assertEqual(like.sender, author2)
        self.assertEqual(like.accepter, author)
        self.assertTrue(like in post.likes.all())
        self.assertTrue(like in author2.liked.all())
        self.assertTrue(ReadPostSerializer(post).data["likes"] == 1)
        
        inbox = Inbox.objects.get(author=author)
        obj = {
            "items": inbox.items.all(),
            "author": inbox.author,
        }
        self.assertTrue(ReadInboxSerializer(obj).data["items"][0] == ReadLikeSerializer(like).data)

    def test_like_comment(self):
        author = create_author("test", "test", "test", "test")
        author2 = create_author("test2", "test2", "test2", "test2")
        post = create_post(author)
        comment_data = {
            "content": "This is a comment",
        }
        comment = CreateCommentSerializer().create(comment_data, author, post)
        like = CreateLikeSerializer().create(
            sender=author2, liked_id=comment.id, is_comment=True, accepter=author
        )
        self.assertEqual(like.liked_id, comment.id)
        self.assertEqual(like.sender, author2)
        self.assertEqual(like.accepter, author)
        self.assertTrue(like in comment.likes.all())
        self.assertTrue(like in author2.liked.all())
        self.assertTrue(ReadCommentSerializer(comment).data["likes"] == 1)
        author3 = create_author("test3", "test3", "test3", "test3")
        like = CreateLikeSerializer().create(
            sender=author3, liked_id=comment.id, is_comment=True, accepter=author
        )
        self.assertTrue(ReadCommentSerializer(comment).data["likes"] == 2)
        # Check inbox for author
        inbox = Inbox.objects.get(author=author)
        obj = {
            "items": inbox.items.all(),
            "author": inbox.author,
        }
        self.assertTrue(ReadInboxSerializer(obj).data["items"][0] == ReadLikeSerializer(like).data)


class InboxTestCase(TestCase):
    def setUp(self) -> None:
        self.author = create_author("test", "test", "test", "test")
        self.author2 = create_author("test2", "test2", "test2", "test2")
        self.post = create_post(self.author)

    def test_add_post(self):
        data = {"item_type": "post", "item_id": self.post.id}
        AddInboxItemSerializer().create(data, self.author2.id, self.author.id)
        inbox = Inbox.objects.get(author=self.author)
        obj = {
            "items": inbox.items.all(),
            "author": inbox.author,
        }
        inbox = ReadInboxSerializer(obj).data
        self.assertTrue(inbox["items"][0] == ReadPostSerializer(self.post).data)

    def test_add_comment(self):
        comment_data = {
            "content": "This is a comment",
        }
        comment = CreateCommentSerializer().create(comment_data, self.author, self.post)
        data = {"item_type": "comment", "item_id": comment.id}
        AddInboxItemSerializer().create(data, self.author2.id, self.author.id)
        inbox = Inbox.objects.get(author=self.author)
        obj = {
            "items": inbox.items.all(),
            "author": inbox.author,
        }
        inbox = ReadInboxSerializer(obj).data
        self.assertTrue(inbox["items"][0] == ReadCommentSerializer(comment).data)

    def test_add_like(self):
        like = CreateLikeSerializer().create(
            sender=self.author2,
            liked_id=self.post.id,
            is_comment=False,
            accepter=self.author,
        )
        data = {"item_type": "like", "item_id": like.id}
        AddInboxItemSerializer().create(data, self.author2.id, self.author.id)
        inbox = Inbox.objects.get(author=self.author)
        obj = {
            "items": inbox.items.all(),
            "author": inbox.author,
        }
        inbox = ReadInboxSerializer(obj).data
        self.assertTrue(inbox["items"][0] == ReadLikeSerializer(like).data)

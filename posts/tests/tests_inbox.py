from authors.serializers import AuthorSerializer
from posts.serializers import ReadCommentSerializer, ReadPostSerializer
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
            "/authors/" + self.author.id + "/posts",
            POST_DATA,
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.client.force_login(self.author2)
        response = self.client.get("/authors/" + self.author2.id + "/inbox")
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(len(response_data["items"]), 1)
        self.assertEqual(response_data["items"][0]["type"], "post")

    def test_add_comment_declarative(self):
        post = create_post(self.author)
        self.client.force_login(self.author2)
        response = self.client.post(
            "/authors/" + self.author.id + "/posts/" + post.id + "/comments",
            {"comment": "test comment"},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.client.force_login(self.author)
        response = self.client.get("/authors/" + self.author.id + "/inbox")
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(len(response_data["items"]), 1)
        self.assertEqual(response_data["items"][0]["type"], "comment")

    def test_add_comment_imperative(self):
        post = create_post(self.author)
        self.client.force_login(self.author2)
        response = self.client.post(
            "/authors/" + self.author.id + "/inbox",
            {
                "type": "comment",
                "post_id": post.id,
                "comment": "test comment",
                "author": AuthorSerializer(self.author2).data,
            },
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)
        self.client.force_login(self.author)
        response = self.client.get("/authors/" + self.author.id + "/inbox")
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(len(response_data["items"]), 1)
        self.assertEqual(response_data["items"][0]["type"], "comment")
        response = self.client.get(
            "/authors/" + self.author.id + "/posts/" + post.id + "/comments"
        )
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(len(response_data), 1)

    def test_add_like_post(self):
        post = create_post(self.author)
        self.client.force_login(self.author2)
        response = self.client.post(
            "/authors/" + self.author.id + "/inbox",
            json.dumps(
                {
                    "summary": "Lara Croft Likes your post",
                    "type": "like",
                    "author": {
                        "type": "author",
                        "id": "http://127.0.0.1:5454/authors/9de17f29c12e8f97bcbbd34cc908f1baba40658e",
                        "host": "http://127.0.0.1:5454/",
                        "displayName": "Lara Croft",
                        "url": "http://127.0.0.1:5454/authors/9de17f29c12e8f97bcbbd34cc908f1baba40658e",
                        "github": "http://github.com/laracroft",
                        "profileImage": "https://i.imgur.com/k7XVwpB.jpeg",
                    },
                    "object": ReadPostSerializer(post).data["id"],
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)
        self.client.force_login(self.author)
        response = self.client.get("/authors/" + self.author.id + "/inbox")
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(len(response_data["items"]), 1)
        self.assertEqual(response_data["items"][0]["type"], "like")
        # Check that the post has a like
        response = self.client.get(
            "/authors/" + self.author.id + "/posts/" + post.id + "/likes"
        )
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(len(response_data), 1)
        
    def test_add_like_comment(self):
        author = create_author("test", "test", "test", "test4")
        author2 = create_author("test2", "test2", "test2", "test22")
        post = create_post(author)
        self.client.force_login(author2)
        comment = self.client.post(
            "/authors/" + author.id + "/posts/" + post.id + "/comments",
            {"comment": "test comment"},
        )
        
        
        self.client.force_login(author2)
        response = self.client.post(
            "/authors/" + author.id + "/inbox",
            json.dumps(
                {
                    "summary": "Lara Croft Likes your post",
                    "type": "like",
                    "author": {
                        "type": "author",
                        "id": "http://127.0.0.1:5454/authors/9de17f29c12e8f97bcbbd34cc908f1baba40658e",
                        "host": "http://127.0.0.1:5454/",
                        "displayName": "Lara Croft",
                        "url": "http://127.0.0.1:5454/authors/9de17f29c12e8f97bcbbd34cc908f1baba40658e",
                        "github": "http://github.com/laracroft",
                        "profileImage": "https://i.imgur.com/k7XVwpB.jpeg",
                    },
                    "object": comment.json()["id"],
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)
        self.client.force_login(author)
        response = self.client.get("/authors/" + author.id + "/inbox")
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(len(response_data["items"]), 2)
        self.assertEqual(response_data["items"][0]["type"], "like")
        # Check that the comment has a like
        response = self.client.get(
             comment.json()["id"] + "/likes"
        )
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(len(response_data), 1)
        

    def test_send_to_inbox(self):
        self.client.force_login(self.author2)
        # send a post to the inbox
        post = create_post(self.author)

        self.client.post(
            "/authors/" + self.author.id + "/inbox",
            ReadPostSerializer(post).data,
            content_type="application/json",
        )
        self.client.force_login(self.author)
        response = self.client.get("/authors/" + self.author.id + "/inbox")
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(len(response_data["items"]), 1)

    def test_clear_inbox(self):
        self.client.force_login(self.author2)
        # send a post to the inbox
        for i in range(10):
            post = create_post(self.author)
            self.client.post(
                "/authors/" + self.author.id + "/inbox",
                ReadPostSerializer(post).data,
                content_type="application/json",
            )
        self.client.force_login(self.author)
        response = self.client.get(
            "/authors/" + self.author.id + "/inbox?page=1&size=10"
        )
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(len(response_data["items"]), 10)
        response = self.client.delete("/authors/" + self.author.id + "/inbox")
        self.assertEqual(response.status_code, 200)
        response = self.client.get("/authors/" + self.author.id + "/inbox")

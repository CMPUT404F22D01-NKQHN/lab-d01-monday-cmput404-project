from .utils import *


class PostTestCase(TestCase):
    def test_create_post(self):
        author = create_author("test", "test", "test", "test")
        self.client.force_login(author)
        response = self.client.post(
            "/authors/" + author.id + "/posts",
            POST_DATA,
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)

    def test_create_post_unauthorized(self):
        author = create_author("test", "test", "test", "test")
        author2 = create_author("test2", "test2", "test2", "test2")
        self.client.force_login(author2)
        response = self.client.post(
            "/authors/" + author.id + "/posts",
            POST_DATA,
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 403)

    def test_get_post(self):
        author = create_author("test", "test", "test", "test")
        post = create_post(author)
        response = self.client.get(
            "/authors/" + author.id + "/posts/" + post.id
        )
        self.assertEqual(response.status_code, 200)

    def test_get_post_dne(self):
        author = create_author("test", "test", "test", "test")
        response = self.client.get(
            "/authors/" + author.id + "/posts/1"
        )
        self.assertEqual(response.status_code, 404)

    def test_get_post_unauthorized(self):
        author = create_author("test", "test", "test", "test")
        post = create_post(author, POST_DATA_2)
        author2 = create_author("test2", "test2", "test2", "test2")
        self.client.force_login(author2)
        response = self.client.get(
            "/authors/" + author.id + "/posts/" + post.id
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
            "/authors/" + author.id + "/posts/" + post.id,
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
            "/authors/" + author.id + "/posts/" + post.id,
            update_data,
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 403)

    def test_delete_post(self):
        author = create_author("test", "test", "test", "test")
        post = create_post(author)
        self.client.force_login(author)
        response = self.client.delete(
            "/authors/" + author.id + "/posts/" + post.id
        )
        self.assertEqual(response.status_code, 204)

    def test_delete_post_unauthorized(self):
        author = create_author("test", "test", "test", "test")
        post = create_post(author)
        author2 = create_author("test2", "test2", "test2", "test2")
        self.client.force_login(author2)
        response = self.client.delete(
            "/authors/" + author.id + "/posts/" + post.id
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
        response = self.client.get("/authors/" + author.id + "/posts")
        self.assertEqual(response.status_code, 200)
        response_data = response.json()

        self.assertEqual(len(response_data["items"]), 2)

    def test_get_posts_by_author_public(self):
        author = create_author("test", "test", "test", "test")
        create_post(author)
        create_post(author, POST_DATA_2)
        author2 = create_author("test2", "test2", "test2", "test2")
        self.client.force_login(author2)
        response = self.client.get("/authors/" + author.id + "/posts")
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(len(response_data["items"]), 1)

    def test_get_posts_by_author_dne(self):
        author = create_author("test", "test", "test", "test")
        self.client.force_login(author)
        response = self.client.get("/authors/1/posts")
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
            "/authors/" + author.id + "/posts",
            post_data,
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(response_data["contentType"], "image/png;base64")
        # Get the post and check the image
        response = self.client.get(response_data["id"])
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        # Get the image from the url in the content
        response = self.client.get(response_data["content"])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.content.replace(b'"', b""),
            base64_image.replace(b'"', b""),
        )
        # Check the image is cached
        response = self.client.get(response_data["content"])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.headers["Cache-Control"], "max-age=86400")

from .utils import *


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

    def test_like_post_unauthorized(self):
        author = create_author("test", "test", "test", "test")
        author2 = create_author("test2", "test2", "test2", "test2")
        post = create_post(author, POST_DATA_2)
        self.client.force_login(author2)
        response = self.client.post(
            "/authors/" + str(int(author.id)) + "/posts/" + str(int(post.id)) + "/likes"
        )
        self.assertEqual(response.status_code, 403)

    def test_like_comment_unauthorized(self):
        author = create_author("test", "test", "test", "test")
        author2 = create_author("test2", "test2", "test2", "test2")
        post = create_post(author, POST_DATA_2)
        self.client.force_login(author)
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
        self.client.force_login(author2)
        response = self.client.post(comment_id + "/likes")
        self.assertEqual(response.status_code, 403)

    def test_like_post_dne(self):
        author = create_author("test", "test", "test", "test")
        author2 = create_author("test2", "test2", "test2", "test2")
        post = create_post(author)
        self.client.force_login(author2)
        response = self.client.post(
            "/authors/" + str(int(author.id)) + "/posts/" + str(int(1)) + "/likes"
        )
        self.assertEqual(response.status_code, 404)
        
    def test_like_comment_dne(self):
        author = create_author("test", "test", "test", "test")
        author2 = create_author("test2", "test2", "test2", "test2")
        post = create_post(author)
        self.client.force_login(author2)
        response = self.client.post(
            "/authors/" + str(int(author.id)) + "/posts/" + str(int(post.id)) + "/comments/" + str(int(1)) + "/likes"
        )
        self.assertEqual(response.status_code, 404)
    
    def test_unlike_post(self):
        author = create_author("test", "test", "test", "test")
        author2 = create_author("test2", "test2", "test2", "test2")
        post = create_post(author)
        self.client.force_login(author2)
        response = self.client.post(
            "/authors/" + str(int(author.id)) + "/posts/" + str(int(post.id)) + "/likes"
        )
        
        self.assertEqual(response.status_code, 200)
        
        response = self.client.delete(
            "/authors/" + str(int(author.id)) + "/posts/" + str(int(post.id)) + "/likes")
        
        self.assertEqual(response.status_code, 204)
    def test_unlike_comment(self):
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
        response = self.client.delete(comment_id + "/likes")
        self.assertEqual(response.status_code, 204)
    def test_get_likes_post(self):
        author = create_author("test", "test", "test", "test")
        author2 = create_author("test2", "test2", "test2", "test2")
        post = create_post(author)
        self.client.force_login(author2)
        response = self.client.post(
            "/authors/" + str(int(author.id)) + "/posts/" + str(int(post.id)) + "/likes"
        )
        self.assertEqual(response.status_code, 200)
        response = self.client.get(
            "/authors/" + str(int(author.id)) + "/posts/" + str(int(post.id)) + "/likes"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
    def test_get_likes_comment(self):
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
        response = self.client.get(comment_id + "/likes")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
        

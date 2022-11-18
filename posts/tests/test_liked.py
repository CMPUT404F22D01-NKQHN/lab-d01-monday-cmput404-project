from .utils import *


class LikedTestCase(TestCase):
    def setUp(self) -> None:
        self.author = create_author("test", "test", "test", "test")
        self.author2 = create_author("test2", "test2", "test2", "test2")

    def author_2_like(self, post):
        self.client.force_login(self.author2)
        response = self.client.post(
            "/authors/"
            + str(int(self.author.id))
            + "/posts/"
            + str(int(post.id))
            + "/likes"
        )

        return response

    def test_liked_post(self):
        for i in range(5):
            post = create_post(self.author)
            self.author_2_like(post)
        response = self.client.get("/authors/" + str(int(self.author2.id)) + "/liked")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 5)

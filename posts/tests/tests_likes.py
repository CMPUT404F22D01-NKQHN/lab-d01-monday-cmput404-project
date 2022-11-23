from .utils import *


class LikesTestCase(TestCase):
    # TODO: Redo
    def test_likes(self):
        author1 = create_author("author1", "author1", "author1", "author1")
        author2 = create_author("author2", "author2", "author2", "author2")
        post = create_post(author1)
        
        
        
        

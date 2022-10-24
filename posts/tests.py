from django.test import TestCase
from authors.models import Author

from posts.models import Comment, Post
from posts.serializers import CreateCommentSerializer, CreatePostSerializer, ReadCommentSerializer

def create_author(display_name, email, password, username):
    return Author.objects.create(
        display_name=display_name,
        email=email,
        password=password,
        username=username,
    )
def create_post(author):
  return CreatePostSerializer().create({
    'title': 'title',
    'source': 'source',
    'origin': 'origin',
    'description': 'description',
    'unlisted': False,
    'author_id': author.id,
    'visibility': 'PUBLIC',
    'contentType': 'text/plain',
    'content': 'content',
  })
class CommentsTestCase(TestCase):
  def test_add_comment_to_post(self):
    author = create_author("test", "test", "test", "test")
    post = create_post(author)
    comment_data = {
      "post_id": post.id,
      "content": "This is a comment",
      "author_id": author.id,
    }
    comment = CreateCommentSerializer().create(comment_data)
    self.assertEqual(comment.post_id, post.id)
    self.assertTrue(comment in post.comments.all())
  
  def test_reply_to_comment(self):
    author = create_author("test", "test", "test", "test")
    post = create_post(author)
    comment_data = {
      "post_id": post.id,
      "content": "This is a comment",
      "author_id": author.id,
    }
    comment = CreateCommentSerializer().create(comment_data)
    reply_data = {
      "post_id": post.id,
      "content": "This is a reply",
      "author_id": author.id,
      "reply_to": comment.id,
    }
    reply = CreateCommentSerializer().create(reply_data)
    self.assertEqual(reply.reply_to, comment.id)
    self.assertTrue(reply in comment.replies.all())
    
class PostTestCase(TestCase):
  def test_create_post(self):
    author = create_author("test", "test", "test", "test")
    post = create_post(author)
    self.assertEqual(post.author, author)
    
    
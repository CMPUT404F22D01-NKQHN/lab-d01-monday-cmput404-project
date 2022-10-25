from django.test import TestCase
from authors.models import Author

from posts.models import Comment, Post
from posts.serializers import CreateCommentSerializer, CreateLikeSerializer, CreatePostSerializer, ReadCommentSerializer, ReadLikeSerializer, ReadPostSerializer

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
  
class LikeTestCase(TestCase):
  def test_like_post(self):
    author = create_author("test", "test", "test", "test")
    author2 = create_author("test2", "test2", "test2", "test2")
    post = create_post(author)
    like_data = {
      "liked_id": post.id,
      "sender_id": author.id,
      "is_comment": False,
      "accepter_id": author2.id,
    }
    like = CreateLikeSerializer().create(like_data)
    self.assertEqual(like.liked_id, post.id)
    self.assertEqual(like.sender, author)
    self.assertEqual(like.accepter, author2)
    self.assertTrue(like in post.likes.all())
    self.assertTrue(like in author.liked.all())
    self.assertTrue(ReadPostSerializer(post).data['likes']==1)
    
  def test_like_comment(self):
    author = create_author("test", "test", "test", "test")
    author2 = create_author("test2", "test2", "test2", "test2")
    post = create_post(author)
    comment_data = {
      "post_id": post.id,
      "content": "This is a comment",
      "author_id": author.id,
    }
    comment = CreateCommentSerializer().create(comment_data)
    like_data = {
      "liked_id": comment.id,
      "sender_id": author.id,
      "is_comment": True,
      "accepter_id": author2.id,
    }
    like = CreateLikeSerializer().create(like_data)
    self.assertEqual(like.liked_id, comment.id)
    self.assertEqual(like.sender, author)
    self.assertEqual(like.accepter, author2)
    self.assertTrue(like in comment.likes.all())
    self.assertTrue(like in author.liked.all())
    self.assertTrue(ReadCommentSerializer(comment).data['likes']==1)
    author3 = create_author("test3", "test3", "test3", "test3")
    like_data = {
      "liked_id": comment.id,
      "sender_id": author3.id,
      "is_comment": True,
      "accepter_id": author2.id,
    }
    like = CreateLikeSerializer().create(like_data)
    self.assertTrue(ReadCommentSerializer(comment).data['likes']==2)
    print(ReadLikeSerializer(like).data)
    
      
    
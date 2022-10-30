import enum
from django.db import models
from django.db import models
import uuid
from authors.models import Author
import enum


    # text/markdown -- common mark
    # text/plain -- UTF-8
    # application/base64
    # image/png;base64
    # image/jpeg;base64 
names = ["COMMON_MARK", "UTF_8", "BASE_64", "PNG_BASE_64", "JPEG_BASE_64", "HTML"]
types = ["text/markdown", "text/plain", "application/base64", "image/png;base64", "image/jpeg;base64", "text/html"]
enum_content_types = enum.Enum("content_types", list(zip(names, types)))
# Create your models here.
class Post(models.Model):
    id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    title = models.CharField(max_length = 500)
    source = models.CharField(max_length = 500, blank = True)
    origin = models.CharField(max_length = 500, blank = True)
    published = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length = 500, blank = True)
    unlisted = models.BooleanField(default = False)
    contentType = models.CharField(max_length = 500, choices = [(name, name) for name in names])
    content = models.CharField(max_length = 2000, blank = True)
    visibility = models.TextField(max_length = 200)
    author = models.ForeignKey('authors.Author', on_delete=models.DO_NOTHING)
    categories = models.ManyToManyField('posts.Category', blank = True)
    comments = models.ManyToManyField('posts.Comment', blank = True)
    likes = models.ManyToManyField('posts.Like', blank = True)
    
class Comment(models.Model):
    id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    post_id = models.UUIDField(editable = False)
    replies = models.ManyToManyField('posts.Comment', blank = True)
    reply_to = models.UUIDField(blank = True, null = True)
    content = models.TextField(max_length = 200)
    author = models.ForeignKey('authors.Author', on_delete=models.DO_NOTHING)
    published = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField('posts.Like', blank = True)

class Like(models.Model):
    id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    liked_id = models.UUIDField(editable = False)
    sender = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='likes_sender')
    accepter = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='likes_accepter')
    is_comment = models.BooleanField(default = False)
    published = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        sender:Author = self.sender
        accepter:Author = self.accepter
        return sender.display_name + 'Likes your post' + accepter.display_name
    
class Category(models.Model):
    name = models.CharField(max_length = 300)
    
class Inbox(models.Model):
    id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    author = models.ForeignKey('authors.Author', on_delete=models.CASCADE)
    items = models.ManyToManyField('posts.InboxItem')

# Enum for inbox item types
item_types = enum.Enum('item_types', 'post comment like follow unfollow friendrequest friendrequestaccept friendrequestreject')
class InboxItem(models.Model):
    # Can be a post, comment, friend request, or like
    id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    item_type = models.CharField(max_length = 20, choices = [(tag, tag.value) for tag in item_types])
    item_id = models.UUIDField(editable = False)
    author = models.ForeignKey('authors.Author', on_delete=models.CASCADE)
    published = models.DateTimeField(auto_now_add=True)
    
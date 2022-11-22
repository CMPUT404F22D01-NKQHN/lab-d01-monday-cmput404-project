import enum
from django.db import models
from django.db import models
import uuid
from authors.models import Author
import enum
from cmput404_project.storage_backends import MediaStorage
from cmput404_project.utilities import gen_id


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
    id = models.CharField(primary_key = True, default = gen_id, editable = False, max_length = 100)
    title = models.CharField(max_length = 500)
    source = models.CharField(max_length = 500, blank = True)
    origin = models.CharField(max_length = 500, blank = True)
    published = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length = 500, blank = True)
    unlisted = models.BooleanField(default = False)
    contentType = models.CharField(max_length = 500, choices = [(tag.name, tag.value) for tag in enum_content_types], default = "text/plain")
    content = models.CharField(max_length = 500, blank = True)
    file = models.FileField(upload_to='files/', blank = True, null = True, storage=MediaStorage())
    visibility = models.TextField(max_length = 200)
    author = models.ForeignKey('authors.Author', on_delete=models.DO_NOTHING)
    categories = models.ManyToManyField('posts.Category', blank = True)
    comments = models.ManyToManyField('posts.Comment', blank = True)
    likes = models.ManyToManyField('posts.Like', blank = True)
    
class Comment(models.Model):
    id = models.CharField(primary_key = True, default = gen_id, editable = False, max_length = 100)
    post_id = models.CharField(editable = False, max_length = 100)
    comment = models.TextField(max_length = 200)
    contentType = models.CharField(max_length = 500, choices = [(tag.name, tag.value) for tag in enum_content_types], default = "text/plain")
    author = models.JSONField(default = dict)
    published = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField('posts.Like', blank = True)

class Like(models.Model):
    id = models.CharField(primary_key = True, default = gen_id, editable = False, max_length = 100)
    object = models.CharField(editable = False, max_length = 400, blank = True)
    author = models.JSONField(default = dict)
    is_comment = models.BooleanField(default = False)
    published = models.DateTimeField(auto_now_add=True)
    
class Category(models.Model):
    name = models.CharField(max_length = 300)
    id = models.CharField(primary_key = True, default = gen_id, editable = False, max_length = 100)
    
class Inbox(models.Model):
    id = models.UUIDField(primary_key = True, default = gen_id, editable = False)
    author = models.ForeignKey('authors.Author', on_delete=models.CASCADE)
    items = models.ManyToManyField('posts.InboxItem')

# Enum for inbox item types
item_types = enum.Enum('item_types', 'post comment like follow unfollow friendrequest friendrequestaccept friendrequestreject')
class InboxItem(models.Model):
    # Can be a post, comment, friend request, or like
    id = models.UUIDField(primary_key = True, default = gen_id, editable = False)
    item = models.JSONField(default = dict)
    published = models.DateTimeField(auto_now_add=True)
    
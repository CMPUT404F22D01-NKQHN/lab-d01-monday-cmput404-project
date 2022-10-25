from django.db import models
from django.db import models
import uuid
from authors.models import Author
# Create your models here.
class Post(models.Model):
    id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    title = models.CharField(max_length = 500)
    source = models.CharField(max_length = 500, blank = True)
    origin = models.CharField(max_length = 500, blank = True)
    published = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length = 500, blank = True)
    unlisted = models.BooleanField(default = False)
    contentType = models.TextField(max_length = 200)
    content = models.CharField(max_length = 2000, blank = True)
    visibility = models.TextField(max_length = 200)
    author = models.ForeignKey('authors.Author', on_delete=models.DO_NOTHING)
    categories = models.ManyToManyField('posts.Category')
    comments = models.ManyToManyField('posts.Comment')
    #likes = models.ManyToManyField('posts.Likes')
    
class Comment(models.Model):
    id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    post_id = models.UUIDField(editable = False)
    replies = models.ManyToManyField('posts.Comment')
    reply_to = models.UUIDField(blank = True, null = True)
    content = models.TextField(max_length = 200)
    author = models.ForeignKey('authors.Author', on_delete=models.DO_NOTHING)
    published = models.DateTimeField(auto_now_add=True)

class Likes(models.Model):
    id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    context = models.CharField(max_length = 200)
    summary = models.CharField(max_length = 100)
    liked_id = models.UUIDField(editable = False)
    author = models.ForeignKey('authors.Author', on_delete = models.CASCADE)
    url = models.CharField(max_length = 100)
    object = models.CharField(max_length = 200)
    sender = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='likes_sender')
    accepter = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='likes_accepter')
    is_comment = models.BooleanField(default = False)

    def __str__(self):
        sender:Author = self.sender
        accepter:Author = self.accepter
        return sender.display_name + 'Likes your post' + accepter.display_name
    
class Category(models.Model):
    name = models.CharField(max_length = 300)
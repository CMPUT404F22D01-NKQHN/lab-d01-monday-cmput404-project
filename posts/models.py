from django.db import models
from django.db import models
import uuid
# Create your models here.
class Post(models.Model):
    id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    title = models.CharField(max_length = 500)
    source = models.CharField(max_length = 500, blank = True)
    origin = models.CharField(max_length = 500, blank = True)
    published = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length = 500, blank = True)
    unlisted = models.BooleanField(default = False)
    contentType = models.TextField(max_length = 2000)
    content = models.CharField(max_length = 200, blank = True)
    visibility = models.TextField(max_length = 2000)
    author = models.ForeignKey('authors.Author', on_delete = models.CASCADE)
    
    # todo: Adding later
    # comments = models.ForeignKey(
    # categories = models.ForeignKey('')
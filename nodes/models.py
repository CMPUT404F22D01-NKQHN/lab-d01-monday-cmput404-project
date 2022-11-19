from django.db import models
from authors.models import Author

# Create your models here.
class Node(models.Model):
    api_url = models.URLField(primary_key=True)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    proxy_users = models.ManyToManyField(Author, related_name='proxy_users', blank=True)
    team_account = models.ForeignKey(Author, related_name='team_account', on_delete=models.CASCADE)
    
        
    
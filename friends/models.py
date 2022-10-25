from django.db import models
from authors.models import Author
# Create your models here.
class FriendRequest(models.Model):
    sender = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='sender')
    accepter = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='accepter')
    accepted = models.BooleanField(default = False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        sender:Author = self.sender
        accepter:Author = self.accepter
        return sender.display_name + ' wants to follow ' + accepter.display_name
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['sender', 'accepter'], name='unique_friend_request_combination'
            )
        ]
        permissions = [
            ('can_accept_friend_request', 'Can accept friend request'),
            ('can_reject_friend_request', 'Can reject friend request'),
        ]
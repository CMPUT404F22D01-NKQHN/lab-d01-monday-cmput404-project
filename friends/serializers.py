from statistics import mode
from rest_framework import serializers
from authors.serializers import AuthorSerializer
from authors.models import Author
from posts.models import Inbox
from .models import FriendRequest
from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field
class CreateFriendRequestSerializer(serializers.Serializer):
    accepter_id = serializers.CharField()
    def create(self, sender_id, accepter_id):
        friend_request = FriendRequest.objects.create(sender_id=sender_id, accepter_id=int(accepter_id))
        # Add the friend request to the accepter's inbox
        accepter = Author.objects.get(id=accepter_id)
        inbox, _ = Inbox.objects.get_or_create(author=accepter)
        from posts.serializers import AddInboxItemSerializer
        AddInboxItemSerializer().create(
            {
                "item": FriendRequestSerializer(friend_request).data,
            },author_id=accepter_id)
        return friend_request
class AcceptFriendRequestSerializer(serializers.Serializer):
    friend_id = serializers.CharField()
    
class FriendRequestSerializer(serializers.Serializer):
    type = serializers.SerializerMethodField('get_type')
    summary = serializers.SerializerMethodField('get_summary')
    actor = serializers.SerializerMethodField('get_actor')
    object = serializers.SerializerMethodField('get_object')
    accepted = serializers.BooleanField()
     
    def create(self, sender_id, accepter_id):
        sender = Author.objects.get(id=sender_id)
        accepter = Author.objects.get(id=accepter_id)
        friend_request = FriendRequest(sender=sender, accepter=accepter) 
        friend_request.save()
        return friend_request
    
    def get_type(self, model):
        return 'Follow'
    
    def get_summary(self, model: FriendRequest):
        return str(model)
    
    def get_actor(self, model: FriendRequest):
        return AuthorSerializer(model.sender).data
    
    def get_object(self, model: FriendRequest):
        return AuthorSerializer(model.accepter).data
    
class FollowersSerializer(serializers.Serializer):
    type = serializers.SerializerMethodField('get_type')
    items = serializers.SerializerMethodField('get_items')
    
    def get_type(self, model):
        return 'followers'
    @extend_schema_field(serializers.ListSerializer(child=AuthorSerializer()))
    def get_items(self, model:Author):
        return AuthorSerializer(model.followers, many=True).data
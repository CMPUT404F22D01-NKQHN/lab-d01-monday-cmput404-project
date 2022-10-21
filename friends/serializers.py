from statistics import mode
from rest_framework import serializers
from authors.serializers import AuthorSerializer
from authors.models import Author
from .models import FriendRequest

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
        return 'Followers'
    
    def get_items(self, model:Author):
        return AuthorSerializer(model.followers, many=True).data
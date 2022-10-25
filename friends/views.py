from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import FollowersSerializer, FriendRequestSerializer
from .models import FriendRequest
from authors.models import Author
from django.contrib.auth.decorators import login_required

@api_view(['POST'])
@login_required
def create_friend_request(request):
    sender_id = request.user.id
    accepter_id = request.data['accepter_id']
    friend_request = FriendRequestSerializer().create(sender_id, accepter_id)
    return Response(FriendRequestSerializer(friend_request).data)


@api_view(['GET'])
def get_all_friend_requests(request):
    friend_requests = FriendRequest.objects.all()
    serializer = FriendRequestSerializer(friend_requests, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_authors_friend_requests(request):
    author_id = request.data['author_id']
    friend_requests = FriendRequest.objects.filter(accepter_id=author_id)
    serializer = FriendRequestSerializer(friend_requests, many=True)
    return Response(serializer.data)

@api_view(['PUT'])
@login_required
def accept_friend_request(request):
    author = request.user
    friend_id = request.data['friend_id']
    friend_request = FriendRequest.objects.get(sender=friend_id, accepter=author.id)
    friend_request.accepted = True
    friend_request.save()
    friend = Author.objects.get(id=friend_id)
    author.followers.add(friend)
    return Response(FriendRequestSerializer(friend_request).data)

@api_view(['GET'])
def get_friends(request, author_id):
    author = Author.objects.get(id=int(author_id))
    serializer = FollowersSerializer(author)
    return Response(serializer.data)


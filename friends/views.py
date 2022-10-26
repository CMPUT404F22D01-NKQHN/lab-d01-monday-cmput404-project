from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import (
    CreateFriendRequestSerializer,
    FollowersSerializer,
    FriendRequestSerializer,
)
from .models import FriendRequest
from authors.models import Author
from django.contrib.auth.decorators import login_required
from drf_spectacular.utils import extend_schema,OpenApiExample

@extend_schema(
    request=CreateFriendRequestSerializer,
    responses=FriendRequestSerializer,
)
@api_view(["POST"])
@login_required
def create_friend_request(request):
    try:
        friend_request = CreateFriendRequestSerializer().create(
            sender_id=request.user.id, accepter_id=request.data["accepter_id"]
        )
        return Response(FriendRequestSerializer(friend_request).data)
    except Exception as e:
        return Response(status=400, data={"error": str(e)})

@extend_schema(
    responses=FriendRequestSerializer,
)
@api_view(["GET"])
@login_required
def get_authors_friend_requests(request):
    friend_requests = FriendRequest.objects.filter(accepter_id=request.user.id)
    serializer = FriendRequestSerializer(friend_requests, many=True)
    return Response(serializer.data)

@extend_schema(
    examples=[OpenApiExample(name="Accept",value={"friend_id":1})],
    request=CreateFriendRequestSerializer,
    summary="Accept a friend request, where friend_id is the id of the person who sent the request"
)
@api_view(["PUT"])
@login_required
def accept_friend_request(request):
    try:
        author = request.user
        friend_id = request.data["friend_id"]
        friend_request = FriendRequest.objects.get(sender=friend_id, accepter=author.id)
        friend_request.accepted = True
        friend_request.save()
        friend = Author.objects.get(id=friend_id)
        author.followers.add(friend)
        return Response(FriendRequestSerializer(friend_request).data)
    except FriendRequest.DoesNotExist:
        return Response(status=404, data={"error": "Friend not found"})


@api_view(["GET"])
@login_required
def get_friends(request, author_id):
    author = Author.objects.get(id=int(author_id))
    serializer = FollowersSerializer(author)
    return Response(serializer.data)

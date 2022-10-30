from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

from authors.serializers import AuthorSerializer
from .serializers import (
    AcceptFriendRequestSerializer,
    CreateFriendRequestSerializer,
    FollowersSerializer,
    FriendRequestSerializer,
)
from .models import FriendRequest
from authors.models import Author
from django.contrib.auth.decorators import login_required
from drf_spectacular.utils import extend_schema,OpenApiExample
from rest_framework.generics import GenericAPIView

@extend_schema(
    request=CreateFriendRequestSerializer,
    responses=FriendRequestSerializer,
)
@api_view(["POST"])
@login_required
def create_friend_request(request):
    try:
        friend_request = CreateFriendRequestSerializer().create(
            sender_id=request.user.id, accepter_id=int(request.data["accepter_id"])
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
    request=AcceptFriendRequestSerializer,
    summary="Accept a friend request, where friend_id is the id of the person who sent the request"
)
@api_view(["PUT"])
@login_required
def accept_friend_request(request):
    try:
        author = request.user
        friend_id = int(request.data["friend_id"])
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

class FollowerListAPIView(GenericAPIView):
    def get_serializer_class(self):
        return FollowersSerializer
    
    def get(self, request, author_id):
        author = Author.objects.get(id=int(author_id))
        serializer = FollowersSerializer(author)
        return Response(serializer.data)

class FollowerAPIView(GenericAPIView):
    def get_serializer_class(self):
        if self.request.method == "PUT":
            return AuthorSerializer
        elif self.request.method == "GET":
            return AuthorSerializer
        elif self.request.method == "DELETE":
            return AuthorSerializer
    

    def put(self, request, author_id, follower_id):
        '''
            Add FOREIGN_AUTHOR_ID as a follower of AUTHOR_ID (must be authenticated)
        '''
        try:
            
            # Check if foreign author sent a friend request
            friend_request = FriendRequest.objects.get(
                sender=follower_id, accepter=author_id, accepted=True
            )
            assert friend_request is not None
            # Assert that the user is allowed to add the foreign author as a follower
            assert request.user.id == author_id
            author = Author.objects.get(id=author_id)
            foreign_author = Author.objects.get(id=follower_id)
            author.followers.add(foreign_author)
            return Response(AuthorSerializer(foreign_author).data)
        except FriendRequest.DoesNotExist:
            return Response(status=404, data={"error": "Friend not found"})
        except AssertionError:
            return Response(status=403, data={"error": "Forbidden"})
        except Exception as e:
            return Response(status=400, data={"error": str(e)})
    
    def get(self, request, author_id, follower_id):
        '''
             check if FOREIGN_AUTHOR_ID is a follower of AUTHOR_ID
        '''
        try:
            author = Author.objects.get(id=author_id)
            foreign_author = Author.objects.get(id=follower_id)
            if foreign_author in author.followers.all():
                return Response(AuthorSerializer(foreign_author).data)
            else:
                return Response(status=404, data={"error": "Foreign author not found"})
        except Exception as e:
            return Response(status=400, data={"error": str(e)})
    
    def delete(self, request, author_id, follower_id):
        '''
            remove FOREIGN_AUTHOR_ID as a follower of AUTHOR_ID
        '''
        try:
            assert request.user.id == author_id
            author = Author.objects.get(id=author_id)
            foreign_author = Author.objects.get(id=follower_id)
            author.followers.remove(foreign_author)
            return Response(AuthorSerializer(foreign_author).data)
        except AssertionError:
            return Response(status=403, data={"error": "Forbidden"})
        except Exception as e:
            return Response(status=400, data={"error": str(e)})
    
            
        
    
        

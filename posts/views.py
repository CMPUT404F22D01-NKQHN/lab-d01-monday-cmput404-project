from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Post
from .serializers import ReadPostSerializer, CreatePostSerializer

@api_view(['GET'])
def get_all_posts(request):
    return Response(ReadPostSerializer(Post.objects.all(), many=True).data)

@api_view(['GET'])
def get_post(request, post_id):
    return Response(ReadPostSerializer(Post.objects.get(id=int(post_id))).data)

@api_view(['POST'])
def create_post(request, **kwargs):
    post = CreatePostSerializer().create(request.data)
    return Response(CreatePostSerializer(post).data)

@api_view(['PUT'])
def update_post(request, post_id):
    # TODO: Implement this
    pass

@api_view(['DELETE'])
def delete_post(request, post_id):
    post = Post.objects.get(id=int(post_id))
    post.delete()
    return Response(f"Post {int(post_id)} deleted")

@api_view(['GET'])
def get_posts_by_author(request, author_id):
    return Response(ReadPostSerializer(Post.objects.filter(author_id=int(author_id)), many=True).data)
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Post, Comment
from .serializers import (
    CreateCommentSerializer,
    ReadCommentSerializer,
    ReadPostSerializer,
    CreatePostSerializer,
)
from drf_spectacular.utils import extend_schema


@api_view(["GET"])
def get_all_posts(request):
    return Response(ReadPostSerializer(Post.objects.all(), many=True).data)


@api_view(["GET"])
def get_post(request, post_id):
    return Response(ReadPostSerializer(Post.objects.get(id=int(post_id))).data)


@extend_schema(
    request=CreatePostSerializer,
    responses=ReadPostSerializer,
)
@api_view(["POST"])
def create_post(request, **kwargs):
    post = CreatePostSerializer().create(request.data)
    return Response(ReadPostSerializer(post).data)


@api_view(["PUT"])
def update_post(request, post_id):
    # TODO: Implement this
    pass


@api_view(["DELETE"])
def delete_post(request, post_id):
    post = Post.objects.get(id=int(post_id))
    post.delete()
    return Response(f"Post {int(post_id)} deleted")


@api_view(["GET"])
def get_posts_by_author(request, author_id):
    return Response(
        ReadPostSerializer(
            Post.objects.filter(author_id=int(author_id)), many=True
        ).data
    )

@extend_schema(
    request=CreateCommentSerializer,
    responses=ReadCommentSerializer,
)
@api_view(["POST"])
def comment_post(request):
    comment = CreateCommentSerializer().create(request.data)
    return Response(ReadCommentSerializer(comment).data)


@api_view(["GET"])
def get_all_comments(request):
    return Response(ReadCommentSerializer(Comment.objects.all(), many=True).data)

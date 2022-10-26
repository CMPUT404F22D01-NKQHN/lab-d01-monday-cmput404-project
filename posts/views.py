from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

from authors.models import Author
from .models import Like, Post, Comment
from .serializers import (
    CreateCommentSerializer,
    ReadCommentSerializer,
    ReadPostSerializer,
    CreatePostSerializer,
    ReadLikeSerializer,
    CreateLikeSerializer,
    UpdatePostSerializer
)
from drf_spectacular.utils import extend_schema
from django.contrib.auth.decorators import login_required


@api_view(["GET"])
@extend_schema(
    description="Get all posts",
    responses=ReadPostSerializer,
)
def get_all_posts(request):
    return Response(ReadPostSerializer(Post.objects.all(), many=True).data)


@api_view(["GET"])
@extend_schema(
    description="Get given post",
    responses=ReadPostSerializer,
)
def get_post(request, post_id="", author_id=""):
    return Response(ReadPostSerializer(Post.objects.get(id=int(post_id))).data)


@extend_schema(
    request=CreatePostSerializer,
    responses=ReadPostSerializer,
)
@login_required
@api_view(["POST"])
def create_post(request, author_id):
    try:
        assert int(request.user.id) == int(author_id), "User ID does not match author ID"
        post = CreatePostSerializer().create(request.data)
        return Response(ReadPostSerializer(post).data)
    except AssertionError as e:
        return Response(status=403, data={"error": str(e)})


@api_view(["PUT"])
def update_post(request, post_id):
    """Update The Post"""
    post = Post.objects.get(id = int(post_id))
    update = UpdatePostSerializer(data=request.data)
    if update.is_valid():
        UpdatePostSerializer().update(post, request.data)
    else:
        return Response(update.error_messages)
    return Response(ReadPostSerializer(post).data)


@login_required
@api_view(["DELETE"])
def delete_post(request, post_id):
    try:
        post = Post.objects.get(id=int(post_id))
        assert post.author.id == request.user.id
        post.delete()
        return Response(status=204)
    except AssertionError:
        return Response(status=403)


@api_view(["GET"])
@login_required
def get_posts_by_author(request, author_id):
    follower = Author.objects.get(id=int(author_id)).followers.filter(id=request.user.id).exists()
    if follower:
        posts = ReadPostSerializer(
            Post.objects.filter(author_id=int(author_id)), many=True
        ).data
    else:
        posts = ReadPostSerializer(
            Post.objects.filter(author_id=int(author_id), visibility="PUBLIC"),
            many=True,
        ).data
    return Response(posts)


@extend_schema(
    request=CreateCommentSerializer,
    responses=ReadCommentSerializer,
)
@api_view(["POST"])
@login_required
def comment_post(request):
    try:
        assert request.user.id == request.data["author_id"]
        post = Post.objects.get(id=int(request.data["post_id"]))
        # Check if post is public
        commentable = post.visibility == "PUBLIC" or post.author.id == request.user.id or post.author.followers.filter(id=request.user.id).exists()
        assert commentable, "Post is not commentable"
        comment = CreateCommentSerializer().create(request.data)
        return Response(ReadCommentSerializer(comment).data)
    except AssertionError:
        return Response(status=403)


@api_view(["GET"])
def get_all_comments(request):
    return Response(ReadCommentSerializer(Comment.objects.all(), many=True).data)

@login_required
@api_view(["POST"])
def like_post(request, post_id):
    try:
        post = Post.objects.get(id=int(post_id))
        assert post.visibility == "PUBLIC" or post.author.id == request.user.id or post.author.followers.filter(id=request.user.id).exists()
        like = CreateLikeSerializer().create(request.data)
        return Response(ReadLikeSerializer(like).data)
    except AssertionError:
        return Response(status=403)

@login_required
@api_view(["POST"])
def like_comment(request, comment_id):
    try:
        comment = Comment.objects.get(id=int(comment_id))
        post_id = comment.post_id
        post = Post.objects.get(id=post_id)
        assert post.visibility == "PUBLIC" or post.author.id == request.user.id or post.author.followers.filter(id=request.user.id).exists()
        like = CreateLikeSerializer().create(request.data)
        return Response(ReadLikeSerializer(like).data)
    except AssertionError:
        return Response(status=403)
    
@login_required
@api_view(["GET"])
def get_likes_on_post(request, post_id):
    try:
        post = Post.objects.get(id=int(post_id))
        assert post.visibility == "PUBLIC" or post.author.id == request.user.id or post.author.followers.filter(id=request.user.id).exists()
        likes = ReadLikeSerializer(post.likes, many=True).data
        return Response(likes)
    except AssertionError:
        return Response(status=403)

@login_required
@api_view(["GET"])
def get_likes_on_comment(request, comment_id):
    try:
        comment = Comment.objects.get(id=int(comment_id))
        post_id = comment.post_id
        post = Post.objects.get(id=post_id)
        assert post.visibility == "PUBLIC" or post.author.id == request.user.id or post.author.followers.filter(id=request.user.id).exists()
        likes = ReadLikeSerializer(comment.likes, many=True).data
        return Response(likes)
    except AssertionError:
        return Response(status=403)

@login_required
@api_view(["POST"])
def delete_like(request):
    try:
        like = Like.objects.get(id=int(request.data['like_id']))
        assert like.sender.id == request.user.id
        like.delete()
        return Response(status=204)
    except AssertionError:
        return Response(status=403)


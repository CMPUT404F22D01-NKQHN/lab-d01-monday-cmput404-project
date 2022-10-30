from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

from authors.models import Author
from .models import Inbox, Like, Post, Comment
from .serializers import (
    AddInboxItemSerializer,
    CreateCommentSerializer,
    ReadAuthorsPostsSerializer,
    ReadCommentSerializer,
    ReadInboxSerializer,
    ReadPostSerializer,
    CreatePostSerializer,
    ReadLikeSerializer,
    CreateLikeSerializer,
    UpdatePostSerializer,
)
from drf_spectacular.utils import extend_schema
from django.contrib.auth.decorators import login_required
from rest_framework.generics import GenericAPIView

def get_post(request, post_id="", author_id=""):
    try:
        post = Post.objects.get(id=int(post_id))
        assert (
            post.visibility == "PUBLIC"
            or post.author.id == request.user.id
            or post.author.followers.filter(id=request.user.id).exists()
        ), "Post is not visible to you"
        return Response(ReadPostSerializer(post).data)
    except AssertionError as e:
        return Response(status=403, data={"error": str(e)})
    except Post.DoesNotExist:
        return Response(status=404, data={"error": "Post not found"})

def create_post(request, author_id):
    try:
        assert int(request.user.id) == int(
            author_id
        ), "User ID does not match author ID"
        post = CreatePostSerializer().create(request.data, request.user.id)
        return Response(ReadPostSerializer(post).data)
    except AssertionError as e:
        return Response(status=403, data={"error": str(e)})


def update_post(request, post_id):
    """Update The Post"""
    try:
        post = Post.objects.get(id=int(post_id))
        assert post.author.id == request.user.id, "User ID does not match author ID"
        update = UpdatePostSerializer(data=request.data)
        if update.is_valid():
            UpdatePostSerializer().update(post, request.data)
        else:
            return Response(update.error_messages)
        return Response(ReadPostSerializer(post).data)
    except AssertionError as e:
        return Response(status=403, data={"error": str(e)})
    except Post.DoesNotExist:
        return Response(status=404, data={"error": "Post not found"})


def delete_post(request, post_id):
    try:
        post = Post.objects.get(id=int(post_id))
        assert post.author.id == request.user.id, "User ID does not match author ID"
        post.delete()
        return Response(status=204)
    except AssertionError:
        return Response(status=403, data={"error": "User ID does not match author ID"})
    except Post.DoesNotExist:
        return Response(status=404, data={"error": "Post not found"})


def get_posts_by_author(request, author_id):
    try:
        follower = (
            Author.objects.get(id=int(author_id))
            .followers.filter(id=request.user.id)
            .exists()
        )
        if follower or int(author_id) == int(request.user.id):
            posts = ReadPostSerializer(
                Post.objects.filter(author_id=int(author_id)), many=True
            ).data
        else:
            posts = ReadPostSerializer(
                Post.objects.filter(author_id=int(author_id), visibility="PUBLIC"),
                many=True,
            ).data
        posts = ReadAuthorsPostsSerializer(posts).data
        return Response(posts)
    except Author.DoesNotExist:
        return Response(status=404, data={"error": "Author not found"})

def comment_post(request, author_id, post_id):
    try:
        post = Post.objects.get(id=int(post_id))
        # Check if post is public
        commentable = (
            post.visibility == "PUBLIC"
            or post.author.id == request.user.id
            or post.author.followers.filter(id=request.user.id).exists()
        )
        assert commentable, "Post is not commentable"
        comment = CreateCommentSerializer().create(request.data, request.user, post)
        return Response(ReadCommentSerializer(comment).data)
    except AssertionError as e:
        return Response(status=403, data={"error": str(e)})

def get_all_comments_by_post(request, post_id):
    try:
        post = Post.objects.get(id=int(post_id))
        assert (
            post.visibility == "PUBLIC"
            or post.author.id == request.user.id
            or post.author.followers.filter(id=request.user.id).exists()
        ), "Post is not commentable"
        return Response(
            ReadCommentSerializer(
                Comment.objects.filter(post_id=int(post_id)), many=True
            ).data
        )
    except AssertionError as e:
        return Response(status=403, data={"error": str(e)})

def like_post(request, post_id):
    try:
        post = Post.objects.get(id=int(post_id))
        assert (
            post.visibility == "PUBLIC"
            or post.author.id == request.user.id
            or post.author.followers.filter(id=request.user.id).exists()
        )
        like = CreateLikeSerializer().create(request.user, post.author, False, int(post_id))
        return Response(ReadLikeSerializer(like).data)
    except AssertionError:
        return Response(status=403)

def like_comment(request, comment_id):
    try:
        comment = Comment.objects.get(id=int(comment_id))
        post_id = comment.post_id
        post = Post.objects.get(id=post_id)
        assert (
            post.visibility == "PUBLIC"
            or post.author.id == request.user.id
            or post.author.followers.filter(id=request.user.id).exists()
        )
        like = CreateLikeSerializer().create(request.user, comment.author, True, int(comment_id))
        return Response(ReadLikeSerializer(like).data)
    except AssertionError:
        return Response(status=403)

def get_likes_on_post(request, post_id):
    try:
        post = Post.objects.get(id=int(post_id))
        assert (
            post.visibility == "PUBLIC"
            or post.author.id == request.user.id
            or post.author.followers.filter(id=request.user.id).exists()
        )
        likes = ReadLikeSerializer(post.likes, many=True).data
        return Response(likes)
    except AssertionError:
        return Response(status=403)

def get_likes_on_comment(request, comment_id):
    try:
        comment = Comment.objects.get(id=int(comment_id))
        post_id = comment.post_id
        post = Post.objects.get(id=post_id)
        assert (
            post.visibility == "PUBLIC"
            or post.author.id == request.user.id
            or post.author.followers.filter(id=request.user.id).exists()
        )
        likes = ReadLikeSerializer(comment.likes, many=True).data
        return Response(likes)
    except AssertionError:
        return Response(status=403)

def delete_like(request):
    try:
        like = Like.objects.get(id=int(request.data["like_id"]))
        assert like.sender.id == request.user.id
        like.delete()
        return Response(status=204)
    except AssertionError:
        return Response(status=403)

class PostAPI(GenericAPIView):
    def get_serializer_class(self):
        if self.request.method == "GET":
            return ReadPostSerializer
        elif self.request.method == "POST":
            return CreatePostSerializer
        elif self.request.method == "PUT":
            return UpdatePostSerializer
        
    def get(self, request, author_id, post_id):
        return get_post(request, post_id)
    
    def put(self, request, author_id, post_id):
        return update_post(request, post_id)

    def delete(self, request, author_id, post_id):
        return delete_post(request, post_id)

class LikesListAPIView(GenericAPIView):
    def get_serializer_class(self):
        if self.request.method == "GET":
            return ReadLikeSerializer
        elif self.request.method == "POST":
            return CreateLikeSerializer

    def get(self, request, author_id, post_id, comment_id=None):
        if comment_id:
            return get_likes_on_comment(request, comment_id)
        else:
            return get_likes_on_post(request, post_id)
    
    def post(self, request, author_id, post_id, comment_id=None):
        if comment_id:
            return like_comment(request, comment_id)
        else:
            return like_post(request, post_id)
    def get_queryset(self):
        return []
class PostListAPI(GenericAPIView):
    def get_serializer_class(self):
        if self.request.method == "GET":
            return ReadAuthorsPostsSerializer
        elif self.request.method == "POST":
            return CreatePostSerializer

    def get(self, request, author_id):
        return get_posts_by_author(request, author_id)
    
    @extend_schema(
        request=CreatePostSerializer,
        responses=ReadPostSerializer,
    )
    def post(self, request, author_id):
        return create_post(request, author_id)


class CommentListAPIView(GenericAPIView):
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ReadCommentSerializer
        elif self.request.method == 'POST':
            return CreateCommentSerializer
    def post(self, request, author_id, post_id):
        return comment_post(request,author_id, post_id)
    def get(self, request, author_id, post_id):
        return get_all_comments_by_post(request, post_id)
    def get_queryset(self):
        return []
class LikedListAPIView(GenericAPIView):
    
    def get_serializer_class(self):
        return ReadLikeSerializer
    def get_queryset(self):
        return []
    def get(self, request, author_id):
        try:
            author = Author.objects.get(id=int(author_id))
            assert author.id == request.user.id
            likes = ReadLikeSerializer(author.liked, many=True).data
            return Response(likes)
        except AssertionError:
            return Response(status=403, data={"error": "You are not authorized to view this page."})
        
class InboxAPIView(GenericAPIView):
    def get_serializer_class(self):
        if self.request.method == "GET":
            return ReadInboxSerializer
        elif self.request.method == "POST":
            return AddInboxItemSerializer
        return ReadInboxSerializer
    def get(self, request, author_id):
        try:
            author = Author.objects.get(id=int(author_id))
            assert author.id == request.user.id
            try:
                inbox = Inbox.objects.get(author=author)
            except Inbox.DoesNotExist:
                inbox = Inbox.objects.create(author=author)
            return Response(ReadInboxSerializer(inbox).data)
        except AssertionError:
            return Response(status=403, data={"error": "You are not authorized to view this page."})
    
    def post(self, request, author_id):
        try:
            author = Author.objects.get(id=author_id)
            AddInboxItemSerializer().create(request.data, request.user.id, author.id)
            inbox = Inbox.objects.get(author=author)
            return Response(ReadInboxSerializer(inbox, many=True).data)
        except AssertionError:
            return Response(status=403, data={"error": "You are not authorized to view this page."})
    def delete(self, request, author_id):
        try:
            author = Author.objects.get(id=author_id)
            assert author.id == request.user.id
            inbox = Inbox.objects.get(author=author)
            inbox.items.all().delete()
            return Response(ReadInboxSerializer(inbox, many=True).data)
        except AssertionError:
            return Response(status=403, data={"error": "You are not authorized to view this page."})
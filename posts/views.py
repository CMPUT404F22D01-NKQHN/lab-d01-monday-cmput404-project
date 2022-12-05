import base64
import os
from rest_framework.response import Response
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from posts.openapi_examples import *
from authors.models import Author
from authors.serializers import AuthorSerializer
from cmput404_project.utilities import CustomPagination
from .models import Post, Comment
from .serializers import (
    CreateCommentSerializer,
    ReadAuthorsPostsSerializer,
    ReadCommentSerializer,
    ReadPostCommentsSerializer,
    ReadPostSerializer,
    CreatePostSerializer,
    LikeSerializer,
    UpdatePostSerializer,
)
from drf_spectacular.utils import extend_schema
from rest_framework.generics import GenericAPIView
from drf_spectacular.utils import extend_schema, OpenApiExample

from rest_framework.renderers import BaseRenderer


class ImageRenderer(BaseRenderer):
    # https://www.django-rest-framework.org/api-guide/renderers/
    media_type = "image/*"
    format = "image/*"
    charset = None
    render_style = "binary"

    def render(self, data, accepted_media_type=None, renderer_context=None):
        return data


def get_post(request, post_id="", author_id=""):
    try:
        post = Post.objects.get(id=post_id)
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
        assert request.user.id == author_id, "User ID does not match author ID"
        post = CreatePostSerializer().create(request.data, request.user.id)
        return Response(ReadPostSerializer(post).data)
    except AssertionError as e:
        return Response(status=403, data={"error": str(e)})


def update_post(request, post_id):
    """Update The Post"""
    try:
        post = Post.objects.get(id=post_id)
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
        post = Post.objects.get(id=post_id)
        assert post.author.id == request.user.id, "User ID does not match author ID"
        post.delete()
        return Response(status=204)
    except AssertionError:
        return Response(status=403, data={"error": "User ID does not match author ID"})
    except Post.DoesNotExist:
        return Response(status=404, data={"error": "Post not found"})


def get_posts_by_author(self, request, author_id):
    try:
        follower = (
            Author.objects.get(id=author_id)
            .followers.filter(id=request.user.id)
            .exists()
        )
        if follower or request.user.id == author_id:
            posts = ReadPostSerializer(
                self.paginate_queryset(
                    Post.objects.filter(author_id=author_id).order_by("-published"),
                    request,
                ),
                many=True,
            ).data
        else:
            posts = ReadPostSerializer(
                self.paginate_queryset(
                    Post.objects.filter(
                        author_id=author_id, visibility="PUBLIC"
                    ).order_by("-published"),
                    request,
                ),
                many=True,
            ).data
        posts = ReadAuthorsPostsSerializer(posts).data
        return Response(posts)
    except Author.DoesNotExist:
        return Response(status=404, data={"error": "Author not found"})


def comment_post(request, author_id, post_id):
    """
    This method is used by the comment post endpoint to automatically populate the author field
    """
    try:
        post = Post.objects.get(id=post_id)
        # Check if post is public
        commentable = (
            post.visibility == "PUBLIC"
            or post.author.id == request.user.id
            or post.author.followers.filter(id=request.user.id).exists()
        )
        assert commentable, "Post is not commentable"
        comment = CreateCommentSerializer().create(
            request.data, AuthorSerializer(request.user).data, post
        )
        return Response(ReadCommentSerializer(comment).data)
    except AssertionError as e:
        return Response(status=403, data={"error": str(e)})


def get_all_comments_by_post(self, request, post_id):
    try:
        post = Post.objects.get(id=post_id)
        assert (
            post.visibility == "PUBLIC"
            or post.author.id == request.user.id
            or post.author.followers.filter(id=request.user.id).exists()
        ), "Post is not commentable"
        data = {
            "post": ReadPostSerializer(post).data["id"],
            "comments": ReadCommentSerializer(
                self.paginate_queryset(
                    Comment.objects.filter(post_id=post_id).order_by("-published"),
                    request,
                ),
                many=True,).data,
            "page": int(request.GET.get("page", 1)),
            "size": int(request.GET.get("size", 20))
            }
        return Response(ReadPostCommentsSerializer(data).data)
            
        
    except AssertionError as e:
        return Response(status=403, data={"error": str(e)})


def get_likes_on_post(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
        assert (
            post.visibility == "PUBLIC"
            or post.author.id == request.user.id
            or post.author.followers.filter(id=request.user.id).exists()
        )
        likes = LikeSerializer(post.likes, many=True).data
        return Response(likes)
    except AssertionError:
        return Response(status=403)


def get_likes_on_comment(request, comment_id):
    try:
        comment = Comment.objects.get(id=comment_id)
        post_id = comment.post_id
        post = Post.objects.get(id=post_id)
        assert (
            post.visibility == "PUBLIC"
            or post.author.id == request.user.id
            or post.author.followers.filter(id=request.user.id).exists()
        )
        likes = LikeSerializer(comment.likes, many=True).data
        return Response(likes)
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

    @extend_schema(
        examples=[
            OpenApiExample(
                "Post",
                value=POST_EXAMPLE,
            )
        ],
        description="Get the post with a specific post id",
    )
    def get(self, request, author_id, post_id):
        """
        Get the post
        """
        return get_post(request, post_id)

    @extend_schema(
        examples=[
            OpenApiExample(
                "Post",
                value=POSTS_ADD_EXAMPLE,
            )
        ],
        description="Update a post",
    )
    def put(self, request, author_id, post_id):
        return update_post(request, post_id)

    def delete(self, request, author_id, post_id):
        """
        Delete the post
        """
        return delete_post(request, post_id)


class LikesListAPIView(GenericAPIView):
    def get_serializer_class(self):
        return LikeSerializer

    @extend_schema(
        examples=[
            OpenApiExample(
                "Post Likes",
                value=LIKED_AUTHOR_EXAMPLE,
            ),
            OpenApiExample(
                "Comment Likes",
                value=LIKED_COMMENT_EXAMPLE,
            )
        ],
        description="Get the likes of item",
    )
    def get(self, request, author_id, post_id, comment_id=None):
        if comment_id:
            return get_likes_on_comment(request, comment_id)
        else:
            return get_likes_on_post(request, post_id)
        
    def get_queryset(self):
        return []


class PostListAPI(GenericAPIView):
    def get_serializer_class(self):
        if self.request.method == "GET":
            return ReadAuthorsPostsSerializer
        elif self.request.method == "POST":
            return CreatePostSerializer

    @extend_schema(
        examples=[
            OpenApiExample(
                "Posts",
                value=POST_LIST_EXAMPLE,
            )
        ],
        description="Get list of posts from author",
    )
    def get(self, request, author_id):
        return get_posts_by_author(self, request, author_id)

    pagination_class = CustomPagination

    @extend_schema(
        request=CreatePostSerializer,
        responses=ReadPostSerializer,
        examples=[
            OpenApiExample(
                "Posts",
                value=POSTS_ADD_EXAMPLE,
            )
        ],
        description="Add post to author's posts",
    )
    def post(self, request, author_id):
        return create_post(request, author_id)

    def paginate_queryset(self, queryset, request):
        return self.pagination_class().paginate_queryset(queryset, request, view=self)


class ImageAPI(GenericAPIView):
    renderer_classes = [ImageRenderer]

    @extend_schema(
        examples=[
            OpenApiExample(
                "Post with image",
                value=POST_EXAMPLE,
            )
        ],
        description="Get post's image",
    )
    @method_decorator(cache_page(60 * 60 * 24))
    def get(self, request, author_id, post_id):
        """
        Gets the image of a post
        """
        try:
            post = Post.objects.get(id=post_id)
            assert (
                post.visibility == "PUBLIC"
                or post.author.id == request.user.id
                or post.author.followers.filter(id=request.user.id).exists()
            )

            if os.environ.get("BUCKETEER_AWS_SECRET_ACCESS_KEY", False):
                try:
                    binary_image = base64.b64decode(
                        post.file.read().decode("utf-8").split(",")[1]
                    )
                    return Response(binary_image, content_type=post.contentType)
                except:
                    try:
                        file = open(post.file.name, "rb")
                        binary_image = base64.b64decode(
                            file.read().decode("utf-8").split(",")[1]
                        )
                        return Response(binary_image, content_type=post.contentType)
                    except:
                        return "File not found"
            else:
                file = open(post.file.name, "rb")
                binary_image = base64.b64decode(
                    file.read().decode("utf-8").split(",")[1]
                )
                return Response(binary_image, content_type=post.contentType)
        except AssertionError:
            return Response(status=403)
        except Post.DoesNotExist:
            return Response(status=404, data={"error": "Post not found"})


class CommentListAPIView(GenericAPIView):
    def get_serializer_class(self):
        if self.request.method == "GET":
            return ReadCommentSerializer
        elif self.request.method == "POST":
            return CreateCommentSerializer

    @extend_schema(
        examples=[
            OpenApiExample(
                "Comments",
                value=CREATE_COMMENT_EXAMPLE,
            )
        ],
        description="Add a new comment on a post",
    )
    def post(self, request, author_id, post_id):
        return comment_post(request, author_id, post_id)

    @extend_schema(
        examples=[
            OpenApiExample(
                "Comments",
                value=COMMENTS_EXAMPLE,
            )
        ],
        description="Get the comments on a post",
    )
    def get(self, request, author_id, post_id):
        return get_all_comments_by_post(self, request, post_id)

    def paginate_queryset(self, queryset, request):
        return self.pagination_class().paginate_queryset(queryset, request, view=self)

    pagination_class = CustomPagination

    def get_queryset(self):
        return []


class LikedListAPIView(GenericAPIView):
    pagination_class = CustomPagination

    def get_serializer_class(self):
        return LikeSerializer

    def get_queryset(self):
        return []

    @extend_schema(
        examples=[
            OpenApiExample(
                "Liked",
                value=LIKED_AUTHOR_EXAMPLE,
            )
        ],
        description="Get the liked content of user",
    )
    def get(self, request, author_id):
        try:
            author = Author.objects.get(id=author_id)
            # assert author.id == request.user.id
            # TODO: Do we need to show different liked posts for different users?
            likes = LikeSerializer(author.liked, many=True).data
            return Response(likes)
        except AssertionError:
            return Response(
                status=403, data={"error": "You are not authorized to view this page."}
            )

class CommentAPIView(GenericAPIView):
    def get_serializer_class(self):
        return ReadCommentSerializer

    @extend_schema(
        examples=[
            OpenApiExample(
                "Comments",
                value=SINGLE_COMMENT_EXAMPLE,
            )
        ],
        description="Get a comment from the comments on a post",
    )
    def get(self, request, author_id, post_id, comment_id):
        try:
            comment = Comment.objects.get(id=comment_id)
            post_id = comment.post_id
            post = Post.objects.get(id=post_id)
            assert (
                post.visibility == "PUBLIC"
                or post.author.id == request.user.id
                or post.author.followers.filter(id=request.user.id).exists()
            )
            comment = ReadCommentSerializer(comment).data
            return Response(comment)
        except AssertionError:
            return Response(status=403)
        except Comment.DoesNotExist:
            return Response(status=404, data={"error": "Comment not found"})
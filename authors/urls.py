from django.urls import path

from posts.views import PostAPI, PostListAPI,\
    LikedListAPIView, CommentListAPIView, LikesListAPIView, ImageAPI,CommentAPIView
from posts.inbox_view import InboxAPIView
from . import views
from friends.views import FollowerListAPIView, FollowerAPIView
# redirect method
from django.views.generic.base import RedirectView
urlpatterns = [
    path("", views.AuthorsAPIView.as_view(), name="get_authors"),
    path("<str:author_id>", views.AuthorAPIView.as_view(), name="author"),
    path("<str:author_id>/followers/", FollowerListAPIView.as_view(), name="author_followers"),
    path("<str:author_id>/followers/<str:follower_id>", FollowerAPIView.as_view(), name="get_follower"),
    path("<str:author_id>/liked/", LikedListAPIView.as_view(), name="author_liked"),
    path("<str:author_id>/inbox/", InboxAPIView.as_view(), name="author_inbox"),
    path("<str:author_id>/posts/<str:post_id>", PostAPI.as_view(), name="post_crud"),
    path(
        "<str:author_id>/posts/", PostListAPI.as_view(), name="post_list_crud"
    ),
    path("<str:author_id>/posts/<str:post_id>/comments/", CommentListAPIView.as_view(), name="comment_list"),
    path("<str:author_id>/posts/<str:post_id>/comments/<str:comment_id>", CommentAPIView.as_view(), name="comment_crud"),
    path("<str:author_id>/posts/<str:post_id>/likes/", LikesListAPIView.as_view(), name="like_post"),
    path("<str:author_id>/posts/<str:post_id>/image", ImageAPI.as_view(), name="image"),
    path("<str:author_id>/posts/<str:post_id>/comments/<str:comment_id>/likes/", LikesListAPIView.as_view(), name="like_comment"),
]

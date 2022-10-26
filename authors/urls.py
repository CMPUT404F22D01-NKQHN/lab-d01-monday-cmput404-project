from django.urls import path

from posts.views import PostAPI, PostListAPI, comment_crud
from . import views
from friends.views import get_friends

urlpatterns = [
    path("", views.AuthorsAPIView.as_view(), name="get_authors"),
    path("<int:author_id>", views.AuthorAPIView.as_view(), name="get_author"),
    path("<str:author_id>/followers", get_friends, name="get_followers"),
    path("<str:author_id>/posts/<str:post_id>", PostAPI.as_view(), name="post_crud"),
    path(
        "<str:author_id>/posts", PostListAPI.as_view(), name="post_list_crud"
    ),
    path("<str:author_id>/posts/<str:post_id>/comments", comment_crud, name = "comment_crud")
]

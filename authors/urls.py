from django.urls import path

from posts.views import get_post, get_posts_by_author, create_post
from . import views
from friends.views import get_friends

urlpatterns = [
    path("", views.get_authors, name="get_authors"),
    path("<int:author_id>", views.author, name="get_author"),
    path("<str:author_id>/followers", get_friends, name="get_followers"),
    path("<str:author_id>/posts/<str:post_id>", get_post, name="get_post"),
    path(
        "<str:author_id>/posts", get_posts_by_author, name="get_posts_by_author"
    ),
    path("<str:author_id>/posts", create_post, name="create_post"),
]

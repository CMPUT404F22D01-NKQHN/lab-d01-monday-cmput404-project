from django.urls import path

from posts.views import all_posts, get_post, post_crud
from . import views
from friends.views import get_friends

urlpatterns = [
    path("", views.get_authors, name="get_authors"),
    path("<int:author_id>", views.author, name="author_crud"),
    path("<str:author_id>/followers", get_friends, name="get_followers"),
    path("<str:author_id>/posts/<str:post_id>", post_crud, name="post_crud"),
    path(
        "<str:author_id>/posts", all_posts, name="all_posts"
    )
]

from django.urls import path
from . import views

urlpatterns = [
    path('service/get-all-posts/', views.get_all_posts, name='get_all_posts'),
    path('service/get-post/<str:post_id>', views.get_post, name='get_post'),
    path('service/create-post/', views.create_post, name='create_post'),
    path('service/update-post/<str:post_id>', views.update_post, name='update_post'),
    path('service/delete-post/<str:post_id>', views.delete_post, name='delete_post'),
    path('service/get-posts-by-author/<str:author_id>', views.get_posts_by_author, name='get_posts_by_author'),
]

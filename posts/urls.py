from django.urls import path
from . import views

urlpatterns = [
    path('service/get-all-posts/', views.get_all_posts, name='get_all_posts'),
    path('service/get-post/<str:post_id>', views.get_post, name='get_post'),
    path('service/create-post/', views.create_post, name='create_post'),
    path('service/update-post/<str:post_id>', views.update_post, name='update_post'),
    path('service/delete-post/<str:post_id>', views.delete_post, name='delete_post'),
    path('service/get-posts-by-author/<str:author_id>', views.get_posts_by_author, name='get_posts_by_author'),
    path('service/get-all-comments/', views.get_all_comments, name='get_all_comments'),
    path('service/comment-on-post/', views.comment_post, name='comment_post'),
    path('service/like-post/<str:post_id>', views.like_post, name='like_post'),
    path('service/like-comment/<str:comment_id>', views.like_comment, name='like_comment'),
    path('service/unlike/', views.delete_like, name='unlike_post'),
    path('service/get-likes-on-post/<str:post_id>', views.get_likes_on_post, name='get_likes_on_post'),
    path('service/get-likes-on-comment/<str:comment_id>', views.get_likes_on_comment, name='get_likes_on_comment'),
]   

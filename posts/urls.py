from django.urls import path
from . import views

urlpatterns = [
    path('service/like-post/<str:post_id>', views.like_post, name='like_post'),
    path('service/like-comment/<str:comment_id>', views.like_comment, name='like_comment'),
    path('service/unlike/', views.delete_like, name='unlike_post'),
    path('service/get-likes-on-post/<str:post_id>', views.get_likes_on_post, name='get_likes_on_post'),
    path('service/get-likes-on-comment/<str:comment_id>', views.get_likes_on_comment, name='get_likes_on_comment'),
]   

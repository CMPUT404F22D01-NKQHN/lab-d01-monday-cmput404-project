from django.urls import path
from . import views

urlpatterns = [
    path('create-friend-request/', views.create_friend_request, name='create_friend_request'),
    path('accept-friend-request/', views.accept_friend_request, name='accept_friend_request'),
    path('get-authors-friend/<str:author_id>', views.get_friends, name='get_friends'),
]

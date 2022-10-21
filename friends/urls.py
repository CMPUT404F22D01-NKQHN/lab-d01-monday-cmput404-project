from django.urls import path
from . import views

urlpatterns = [
    path('service/get-all-friend-requests/', views.get_all_friend_requests, name='get_all_friend_requests'),
    path('service/create-friend-request/', views.create_friend_request, name='create_friend_request'),
    path('service/accept-friend-request/', views.accept_friend_request, name='accept_friend_request'),
    path('service/get-authors-friend/<str:author_id>', views.get_friends, name='get_friends'),
]

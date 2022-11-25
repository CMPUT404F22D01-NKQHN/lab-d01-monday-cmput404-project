from django.contrib import admin
from django.urls import path, include
from . import views
from django.shortcuts import redirect
urlpatterns = [
  path('', views.home, name='index'),
  path('profile', views.profile, name='profile'),
  path("logout/", lambda request: redirect("/login/")),
  path('', include('django.contrib.auth.urls')),
  path('inbox', views.inbox, name='inbox'),
  path('followers', views.followers, name='followers'),
  path('user/<str:author_id>', views.user, name='user')
]
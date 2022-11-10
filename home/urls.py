from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
  path('home', views.home, name='index'),
  path('profile', views.profile, name='profile'),
  path('', views.login, name='login'),
  path('register', views.register, name='register'),

  
  # if user is not logged in redirect to login page
  # if user is logged in redirect to home page
  # if user is not signed up redirect to register page


  
]
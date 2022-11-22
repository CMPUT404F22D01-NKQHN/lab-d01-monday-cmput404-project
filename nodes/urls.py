from django.urls import path
from . import views

urlpatterns = [
    path('', views.NodeAPIView.as_view()),
]

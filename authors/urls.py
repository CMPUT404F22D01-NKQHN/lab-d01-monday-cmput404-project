from django.urls import path
from . import views

urlpatterns = [
    path('service/authors/', views.get_authors, name='get_authors'),
    
]

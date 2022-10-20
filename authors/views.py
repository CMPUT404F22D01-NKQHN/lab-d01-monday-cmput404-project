from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import AuthorSerializer
from .models import Author


@api_view(['GET'])
def get_authors(request):
    """Get all authors"""
    authors = Author.objects.all()
    serializer = AuthorSerializer(authors, many=True)
    return Response(serializer.data)

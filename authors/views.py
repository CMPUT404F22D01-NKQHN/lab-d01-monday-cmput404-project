from http.client import HTTPResponse
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.template import loader
from django.http import HttpResponse

import authors
from .serializers import AuthorSerializer
from .models import Author


@api_view(['GET'])
def get_authors(request):
    """Get all authors"""
    authors = Author.objects.all()
    serializer = AuthorSerializer(authors, many=True)
    return Response(serializer.data)

from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import AuthorSerializer, ReadAuthorsSerializer, UpdateAuthorSerializer
from .models import Author
from drf_spectacular.utils import extend_schema


@api_view(['GET'])
def get_authors(request):
    """Get all authors"""
    authors = ReadAuthorsSerializer(Author.objects.all())
    return Response(authors.data)

@api_view(['GET','POST'])
def author(request, author_id):
    if request.method == 'GET':
        return get_author(request, author_id)
    elif request.method == 'POST':
        return update_author(request, author_id)

@api_view(['GET'])
def get_author(request, author_id):
    """Get author"""
    author = Author.objects.get(id=int(author_id))
    return Response(AuthorSerializer(author).data)

@api_view(['POST'])
@extend_schema(
    request=UpdateAuthorSerializer,
    responses=AuthorSerializer,
)
def update_author(request, author_id):
    """Update The Author"""
    author = Author.objects.get(id = int(author_id))
    update = UpdateAuthorSerializer(data=request.data)
    if update.is_valid():
        UpdateAuthorSerializer().update(author, request.data)
    else:
        return Response(update.error_messages)
    return Response(AuthorSerializer(author).data)
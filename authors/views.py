from rest_framework.response import Response

from cmput404_project.utilities import CustomPagination
from .serializers import AuthorSerializer, ReadAuthorsSerializer, UpdateAuthorSerializer
from .models import Author
from drf_spectacular.utils import extend_schema, OpenApiExample
from rest_framework import generics

from authors.openapi_examples import *


class AuthorAPIView(generics.GenericAPIView):
    @extend_schema(
            examples=[
            OpenApiExample(
                "Author",
                value=AUTHOR_SINGLE_EXAMPLE,
            )
        ],
        description="Get an author")
    def get(self, request, author_id):
        try:
            author = Author.objects.get(id=author_id, proxy=False)
            return Response(AuthorSerializer(author).data)
        except Author.DoesNotExist:
            return Response(status=404)
        except Exception as e:
            return Response(status=400)

    @extend_schema(
            request=UpdateAuthorSerializer, 
            responses=AuthorSerializer,
            examples=[
            OpenApiExample(
                "Author",
                value=AUTHOR_SINGLE_UPDATE_EXAMPLE,
            )
        ],
        description="Update an author")
    def post(self, request, author_id):
        try:
            assert request.user.id == author_id, "User ID does not match author ID"
            author = Author.objects.get(id=author_id)
            update = UpdateAuthorSerializer(data=request.data)
            if update.is_valid():
                UpdateAuthorSerializer().update(author, request.data)
            else:
                return Response(update.error_messages)
            return Response(AuthorSerializer(author).data)
        except AssertionError as e:
            return Response(status=403, data={"error": str(e)})

    def get_serializer_class(self):
        return AuthorSerializer


class AuthorsAPIView(generics.GenericAPIView):
    @extend_schema(
        examples=[
            OpenApiExample(
                "Authors",
                value=AUTHORS_EXAMPLE,
            )
        ],
        description="Get list of authors",
    )
    def get(self, request):
        authors = self.paginate_queryset(self.get_queryset(), request)
        return Response(
            ReadAuthorsSerializer(AuthorSerializer(authors, many=True).data).data
        )

    def get_queryset(self):
        return Author.objects.filter(is_another_server=False, proxy=False).order_by("id")

    def paginate_queryset(self, queryset, request):
        return self.pagination_class().paginate_queryset(queryset, request, view=self)

    def get_serializer_class(self):
        return ReadAuthorsSerializer

    pagination_class = CustomPagination

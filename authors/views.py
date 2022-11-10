from rest_framework.response import Response

from cmput404_project.utilities import CustomPagination
from .serializers import AuthorSerializer, ReadAuthorsSerializer, UpdateAuthorSerializer
from .models import Author
from drf_spectacular.utils import extend_schema
from rest_framework import generics


class AuthorAPIView(generics.GenericAPIView):
    def get(self, request, author_id):
        author = Author.objects.get(id=int(author_id))
        return Response(AuthorSerializer(author).data)

    @extend_schema(request=UpdateAuthorSerializer, responses=AuthorSerializer)
    def post(self, request, author_id):
        try:
            assert int(request.user.id) == int(
                author_id
            ), "User ID does not match author ID"
            author = Author.objects.get(id=int(author_id))
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
    def get(self, request):
        authors = self.paginate_queryset(self.get_queryset(), request)
        return Response(
            ReadAuthorsSerializer(AuthorSerializer(authors, many=True).data).data
        )

    def get_queryset(self):
        return Author.objects.all()

    def paginate_queryset(self, queryset, request):
        return self.pagination_class().paginate_queryset(queryset, request, view=self)

    def get_serializer_class(self):
        return ReadAuthorsSerializer

    pagination_class = CustomPagination

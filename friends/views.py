from rest_framework.response import Response

from authors.serializers import AuthorSerializer
from .serializers import (
    FollowersSerializer,
)


from authors.models import Author
from rest_framework.generics import GenericAPIView


class FollowerListAPIView(GenericAPIView):
    def get_serializer_class(self):
        return FollowersSerializer

    def get(self, request, author_id):
        author = Author.objects.get(id=author_id)
        serializer = FollowersSerializer(author)
        return Response(serializer.data)


class FollowerAPIView(GenericAPIView):
    def get_serializer_class(self):
        if self.request.method == "GET":
            return AuthorSerializer
        else:
            return None

    def put(self, request, author_id, follower_id):
        """
        Add FOREIGN_AUTHOR_ID as a follower of AUTHOR_ID (must be authenticated)
        """
        try:
            # Assert that the user is allowed to add the foreign author as a follower
            assert request.user.id == author_id
            author = Author.objects.get(id=author_id)
            foreign_author = Author.objects.get(id=follower_id)
            author.followers.add(foreign_author)
            return Response(AuthorSerializer(foreign_author).data)
        except AssertionError:
            return Response(status=403, data={"error": "Forbidden"})
        except Exception as e:
            return Response(status=400, data={"error": str(e)})

    def get(self, request, author_id, follower_id):
        """
        check if FOREIGN_AUTHOR_ID is a follower of AUTHOR_ID
        """
        try:
            author = Author.objects.get(id=author_id)
            foreign_author = Author.objects.get(id=follower_id)
            if foreign_author in author.followers.all():
                return Response(AuthorSerializer(foreign_author).data)
            else:
                return Response(status=404, data={"error": "Foreign author not found"})
        except Exception as e:
            return Response(status=400, data={"error": str(e)})

    def delete(self, request, author_id, follower_id):
        """
        remove FOREIGN_AUTHOR_ID as a follower of AUTHOR_ID
        """
        try:
            assert request.user.id == author_id
            author = Author.objects.get(id=author_id)
            foreign_author = Author.objects.get(id=follower_id)
            author.followers.remove(foreign_author)
            return Response(AuthorSerializer(foreign_author).data)
        except AssertionError:
            return Response(status=403, data={"error": "Forbidden"})
        except Exception as e:
            return Response(status=400, data={"error": str(e)})

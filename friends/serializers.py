from rest_framework import serializers
from authors.serializers import AuthorSerializer
from authors.models import Author
from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field


class FollowersSerializer(serializers.Serializer):
    type = serializers.SerializerMethodField("get_type")
    items = serializers.SerializerMethodField("get_items")

    def get_type(self, model):
        return "followers"

    @extend_schema_field(serializers.ListSerializer(child=AuthorSerializer()))
    def get_items(self, model: Author):
        return AuthorSerializer(model.followers, many=True).data

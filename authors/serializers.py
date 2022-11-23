from typing import List
from rest_framework import serializers
from .models import Author
import os
from drf_spectacular.utils import extend_schema_field


class AuthorSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField("get_type")
    displayName = serializers.SerializerMethodField("get_display_name")
    github = serializers.CharField(max_length=100, required=False)
    host = serializers.CharField(max_length=500)
    id = serializers.SerializerMethodField("get_id")
    uuid = serializers.SerializerMethodField("get_uuid")
    url = serializers.SerializerMethodField("get_id")
    profileImage = serializers.SerializerMethodField("get_img")

    def create(self, validated_data):
        return Author.objects.create(**validated_data)
    
    def get_display_name(self, model: Author) -> str:
        return model.display_name

    def update(self, instance, validated_data):
        instance.display_name = validated_data.get(
            "display_name", instance.display_name
        )
        instance.github = validated_data.get("github", instance.github)

    def get_type(self, model: Author) -> str:
        return "author"

    def get_id(self, model: Author) -> str:
        return f"{model.host}/authors/{model.id}"
    def get_uuid(self, model: Author) -> str:
        return model.id

    def get_img(self, model: Author) -> str:
        if model.profileImage == "":
            return "https://i.imgur.com/k7XVwpB.jpeg"
        else:
            return model.profileImage

    class Meta:
        model = Author
        fields = ("type", "displayName", "github", "host", "id", "url", "profileImage","uuid")


class ReadAuthorsSerializer(serializers.Serializer):
    type = serializers.SerializerMethodField("get_type")
    items = serializers.SerializerMethodField("get_items")

    def get_type(self, _):
        return "authors"

    @extend_schema_field(serializers.ListSerializer(child=AuthorSerializer()))
    def get_items(self, data) -> List[Author]:
        return data

    class Meta:
        fields = ("type", "items")


class UpdateAuthorSerializer(serializers.ModelSerializer):
    display_name = serializers.CharField(required=False)
    github = serializers.CharField(required=False)
    profileImage = serializers.CharField(required=False)

    def update(self, instance: Author, data):
        if data.get("display_name"):
            instance.display_name = data["display_name"]
        if data.get("github"):
            instance.github = data["github"]
        if data.get("profileImage"):
            instance.profileImage = data["profileImage"]
        instance.save()

    class Meta:
        model = Author
        fields = ("display_name", "github", "profileImage")

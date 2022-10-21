from rest_framework import serializers
from .models import Author
import os
class AuthorSerializer(serializers.Serializer):
    type = serializers.SerializerMethodField('get_type')
    display_name = serializers.CharField(max_length=100)
    github = serializers.CharField(max_length=100, required=False)
    host = serializers.SerializerMethodField('get_host')
    id = serializers.SerializerMethodField('get_id')
    url = serializers.SerializerMethodField('get_id')
    profileImage = serializers.SerializerMethodField('get_img')

    def create(self, validated_data):
        return Author.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.display_name = validated_data.get('display_name', instance.display_name)
        instance.github = validated_data.get('github', instance.github)
    
    def get_type(self, model : Author):
        return 'authors'
    
    def get_host(self, model : Author):
        return os.environ.get('HOSTNAME', 'http://127.0.0.1:5454')

    def get_id(self, model : Author):
        return f"{self.get_host(model)}/{self.get_type(model)}/{int(model.id)}"
    
    def get_img(self, model: Author):
        if model.profileImage == "":
            return "https://i.imgur.com/k7XVwpB.jpeg"
        else:
            return model.profileImage
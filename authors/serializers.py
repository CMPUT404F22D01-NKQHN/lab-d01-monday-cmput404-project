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
        return 'author'
    
    def get_host(self, model : Author):
        return os.environ.get('HOSTNAME', 'http://localhost:8000')

    def get_id(self, model : Author):
        return f"{self.get_host(model)}/{self.get_type(model)}s/{int(model.id)}"
    
    def get_img(self, model: Author):
        if model.profileImage == "":
            return "https://i.imgur.com/k7XVwpB.jpeg"
        else:
            return model.profileImage
        
class ReadAuthorsSerializer(serializers.Serializer):
    type = serializers.SerializerMethodField('get_type')
    items = serializers.SerializerMethodField('get_items')
    
    def get_type(self, model : Author):
        return 'authors'
    
    def get_items(self, model : Author):
        return AuthorSerializer(model, many=True).data


class UpdateAuthorSerializer(serializers.Serializer):
    display_name = serializers.CharField(required = False)
    github = serializers.CharField(required=False)
    profileImage = serializers.CharField(required=False)
    
    def update(self, instance: Author, data):
        if data.get('display_name'):
            instance.display_name = data['display_name']
        if data.get('github'):
            instance.github = data['github']
        if data.get('profileImage'):
            instance.profileImage = data['profileImage']
        instance.save()
        
    class Meta:
        model = Author
        fields = ('display_name', 'github', 'profileImage')
from rest_framework import serializers
from authors.models import Author
from authors.serializers import AuthorSerializer
from .models import Post

class CreatePostSerializer(serializers.ModelSerializer):
    title = serializers.CharField()
    source = serializers.CharField()
    origin = serializers.CharField()
    description = serializers.CharField()
    unlisted = serializers.BooleanField()
    author_id = serializers.CharField()
    visibility = serializers.CharField()
    contentType = serializers.CharField()
    content = serializers.CharField()
    
    def create(self, data):
        author = Author.objects.get(id=data['author_id'])
        del data['author_id']
        data['author'] = author
        post = Post.objects.create(**data)
        return post
    
    class Meta:
        model = Post
        fields = '__all__'
    
class ReadPostSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField('get_type')
    id = serializers.SerializerMethodField('get_id')
    title = serializers.CharField()
    source = serializers.CharField()
    origin = serializers.CharField()
    published = serializers.DateTimeField()
    description = serializers.CharField()
    unlisted = serializers.BooleanField()
    author = serializers.SerializerMethodField('get_author')
    visibility = serializers.CharField()
    contentType = serializers.CharField()
    content = serializers.CharField()
    
    def get_author(self, model: Post):
        author = AuthorSerializer(model.author).data
        return author

    def get_id(self, model: Post):
        author_id = AuthorSerializer(model.author).data["id"]
        return f"{author_id}/posts/{int(model.id)}"
    
    def get_type(self, model):
        return 'Post'
        
    class Meta:
        model = Post
        fields = '__all__'
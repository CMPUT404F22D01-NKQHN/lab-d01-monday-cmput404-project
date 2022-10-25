from rest_framework import serializers
from authors.models import Author
from authors.serializers import AuthorSerializer
from .models import Post,Comment,Likes

class CreatePostSerializer(serializers.ModelSerializer):
    title = serializers.CharField()
    source = serializers.CharField()
    origin = serializers.CharField()
    description = serializers.CharField()
    unlisted = serializers.BooleanField()
    author_id = serializers.IntegerField()
    visibility = serializers.CharField()
    contentType = serializers.CharField()
    content = serializers.CharField()
    
    def create(self, data):
        assert data['visibility'] in ["PUBLIC","FRIENDS"], "Invalid visibility"
        assert data['contentType'] in ["text/markdown","text/plain","application/base64","image/png;base64","image/jpeg;base64"],"Invalid content-type"
        author = Author.objects.get(id=data['author_id'])
        del data['author_id']
        data['author'] = author
        post = Post.objects.create(**data)
        return post
    
    class Meta:
        model = Post
        exclude = ('id', 'published', 'categories', 'comments', 'author')
        
class CreateCommentSerializer(serializers.ModelSerializer):
    content = serializers.CharField()
    reply_to = serializers.IntegerField(required=False)
    post_id = serializers.IntegerField(required=False)
    author = serializers.IntegerField(required=False)
    
    def create(self, data):
        author = Author.objects.get(id=data['author_id'])
        del data['author_id']
        data['author'] = author
        comment = Comment.objects.create(**data)
        post = Post.objects.get(id=data['post_id'])
        post.comments.add(comment)
        if data.get('reply_to'):
            reply_to = Comment.objects.get(id=data['reply_to'])
            reply_to.replies.add(comment)
        return comment

    class Meta:
        model = Comment
        exclude = ('id', 'published', 'replies')

class ReadCommentSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField('get_type')
    author = serializers.SerializerMethodField('get_author')
    
    def get_type(self, obj):
        return "comment"

    def get_author(self, obj):
        return AuthorSerializer(obj.author).data
    class Meta:
        model = Comment
        fields = '__all__'

class LikesSerializer(serializers.ModelSerializer):
    author = serializers.IntegerField(required = False)
    liked_id = serializers.IntegerField(required = False)
    #profileImage = serializers.CharField()
    object = serializers.SerializerMethodField('get_object')
    summary = serializers.SerializerMethodField('get_summary')
    type = serializers.SerializerMethodField('get_type')
    author = serializers.SerializerMethodField('get_author')

    def create(self, data):
        author = Author.objects.get(id = data['author_id'])
        del data['author']
        likes = Likes.objects.create(**data)
        post = Post.object.get(id = data['post_id'])
        post.likes.add(likes)
        return likes
    
    def get_summary(self, model: Likes):
        return str(model)

    def get_object(self, model: Likes):
        if model.is_comment:
            post = Post.objects.filter(comments=model.liked_id).first()
            return f"{model.accepter.id}/{post.id}/comment/{model.liked_id}"
        else:
            return f"{model.accepter.id}/{model.liked_id}"
    class Meta:
        model = Likes
        fields = '__all__'
        
class ReadLikesSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField('get_type')
    author = serializers.SerializerMethodField('get_author')

    def get_type(self, obj):
        return 'Like'

    def get_author(self, obj):
        return AuthorSerializer(obj.author).data
    
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
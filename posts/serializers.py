from rest_framework import serializers
from authors.models import Author
from authors.serializers import AuthorSerializer
from .models import Post,Comment,Like

class UpdatePostSerializer(serializers.Serializer):
    title = serializers.CharField(required=False)
    source = serializers.CharField(required=False)
    origin = serializers.CharField(required=False)
    description = serializers.CharField(required=False)
    unlisted = serializers.BooleanField(required=False)
    visibility = serializers.CharField(required=False)
    contentType = serializers.CharField(required=False)
    content = serializers.CharField(required=False)
    
    def update(self, instance: Post, data):
        if data.get('title'):
            instance.title = data['title']
        if data.get('source'):
            instance.source = data['source']
        if data.get('origin'):
            instance.origin = data['origin']
        if data.get('description'):
            instance.description = data['description']
        if data.get('unlisted'):
            instance.unlisted = data['unlisted']
        if data.get('visibility'):
            instance.visibility = data['visibility']
        if data.get('contentType'):
            instance.contentType = data['contentType']
        if data.get('content'):
            instance.content = data['content']
        instance.save()
        
    class Meta:
        model = Post
        fields = ('title', 'source', 'origin', 'description', 'unlisted',  'visibility', 'contentType', 'content') 

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
    likes = serializers.SerializerMethodField('get_likes')
    def get_type(self, obj):
        return "comment"

    def get_author(self, obj):
        return AuthorSerializer(obj.author).data
    def get_likes(self, obj: Comment):
        return obj.likes.count()
    class Meta:
        model = Comment
        fields = '__all__'

class CreateLikeSerializer(serializers.ModelSerializer):
    sender_id = serializers.IntegerField(required = False)
    accepter_id = serializers.IntegerField(required = False)
    liked_id = serializers.IntegerField()
    
    def create(self, sender, accepter, is_comment, liked_id):
        if is_comment:
            assert Comment.objects.filter(id=liked_id).exists(), "Comment does not exist"
            assert Comment.objects.get(id=liked_id).author == accepter, "Comment does not belong to accepter"
        else:
            assert Post.objects.filter(id=liked_id).exists(), "Post does not exist"
            assert Post.objects.get(id=liked_id).author == accepter, "Post does not belong to accepter"
        
        like = Like.objects.create(sender=sender, accepter=accepter, is_comment=is_comment, liked_id=liked_id)
        if is_comment:
            comment = Comment.objects.get(id=liked_id)
            comment.likes.add(like)
        else:
            post = Post.objects.get(id=liked_id)
            post.likes.add(like)
        sender.liked.add(like)
        return like
    class Meta:
        model = Like
        exclude = ('id')
        
        
class ReadLikeSerializer(serializers.ModelSerializer):
    sender = serializers.SerializerMethodField('get_sender')
    accepter = serializers.SerializerMethodField('get_accepter')
    liked_id = serializers.IntegerField()
    object = serializers.SerializerMethodField('get_object')
    summary = serializers.SerializerMethodField('get_summary')
    type = serializers.SerializerMethodField('get_type')

    def get_sender(self, obj):
        return AuthorSerializer(obj.sender).data
    def get_accepter(self, obj):
        return AuthorSerializer(obj.accepter).data
    def get_object(self, model: Like):
        if model.is_comment:
            post = Post.objects.filter(comments=model.liked_id).first()
            return f"{model.accepter.id}/{post.id}/comment/{model.liked_id}"
        else:
            return f"{model.accepter.id}/{model.liked_id}"
    def get_summary(self, model: Like):
        return str(model)
    def get_type(self, model: Like):
        return "Like"
    class Meta:
        model = Like
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
    likes = serializers.SerializerMethodField('get_likes')
    
    def get_author(self, model: Post):
        author = AuthorSerializer(model.author).data
        return author

    def get_id(self, model: Post):
        author_id = AuthorSerializer(model.author).data["id"]
        return f"{author_id}/posts/{int(model.id)}"
    
    def get_type(self, model):
        return 'Post'
        
    def get_likes(self, model: Post):
        return model.likes.count()
    class Meta:
        model = Post
        fields = '__all__'


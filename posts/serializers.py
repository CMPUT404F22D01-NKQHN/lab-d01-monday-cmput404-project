from typing import List
import requests
import uuid
from rest_framework import serializers
from authors.models import Author
from authors.serializers import AuthorSerializer
from .models import Inbox, InboxItem, Post, Comment, Like
from drf_spectacular.utils import extend_schema_field
import os
from cmput404_project.storage_backends import MediaStorage
import tempfile


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
        if data.get("title"):
            instance.title = data["title"]
        if data.get("source"):
            instance.source = data["source"]
        if data.get("origin"):
            instance.origin = data["origin"]
        if data.get("description"):
            instance.description = data["description"]
        if data.get("unlisted"):
            instance.unlisted = data["unlisted"]
        if data.get("visibility"):
            instance.visibility = data["visibility"]
        if data.get("contentType"):
            instance.contentType = data["contentType"]
        if data.get("content"):
            instance.content = data["content"]
        instance.save()

    class Meta:
        model = Post
        fields = (
            "title",
            "source",
            "origin",
            "description",
            "unlisted",
            "visibility",
            "contentType",
            "content",
        )


class CreatePostSerializer(serializers.ModelSerializer):
    title = serializers.CharField()
    source = serializers.CharField()
    origin = serializers.CharField()
    description = serializers.CharField()
    unlisted = serializers.BooleanField()
    visibility = serializers.CharField()
    contentType = serializers.CharField()
    content = serializers.CharField()

    def create(self, data, author_id):
        assert data["visibility"] in ["PUBLIC", "FRIENDS", "PRIVATE"], "Invalid visibility"
        assert data["contentType"] in [
            "text/markdown",
            "text/plain",
            "text/html",
            "application/base64",
            "image/png;base64",
            "image/jpeg;base64",
        ], "Invalid content-type"
        author = Author.objects.get(id=author_id)
        data["author"] = author
        if data["contentType"] in [
            "application/base64",
            "image/png;base64",
            "image/jpeg;base64",
        ]:
            # convert base 64 encoded data["img"] to png file
            id = uuid.UUID(bytes=os.urandom(16))
            name = os.path.join("files", f"{author_id}_{id}.png")
            if os.environ.get("BUCKETEER_AWS_SECRET_ACCESS_KEY", None):
                # Create temp file
                temp = tempfile.NamedTemporaryFile()
                temp.write(data["content"].encode("utf-8"))
                media_file = MediaStorage()
                media_file.save(name, temp)
            else:
                name = os.path.join("./media", name)
                # Ensure directory exists
                os.makedirs(os.path.dirname(name), exist_ok=True)
                with open(name, "w") as f:
                    f.write(data["content"])
            data["content"] = ""

            data["file"] = name

        post = Post.objects.create(**data)
        # Add inbox item for all followers
        data = ReadPostSerializer(post).data
        for follower in author.followers.all():
            AddInboxItemSerializer().create(data, follower.id)
            # TODO: Refactor to send inbox items to remote servers
            # res = requests.post(
            #     f"{follower.host}/{follower.id}/inbox",
            #     json = {
            #         "type": "post",
            #         "actor": AuthorSerializer(author).data,
            #         "post": ReadPostSerializer(post).data,
            #     },
            # )

        return post

    class Meta:
        model = Post
        exclude = ("id", "published", "categories", "comments", "author", "likes", "file")


class CreateCommentSerializer(serializers.ModelSerializer):
    comment = serializers.CharField()
    contentType = serializers.CharField()

    def create(self, data, author, post):
        comment = Comment.objects.create(
            comment=data["comment"],
            author=author,
            post_id=post.id,
            contentType=data.get("contentType", "text/plain"),
        )
        post.comments.add(comment)
        post.save()
        # Add inbox item to original author
        data = ReadCommentSerializer(comment).data
        AddInboxItemSerializer().create(
            data,
            post.author.id,
        )

        return comment

    class Meta:
        model = Comment
        exclude = ("id", "published", "likes", "author")


class CommentInboxItemSerializer(serializers.Serializer):
    type = serializers.CharField()
    author = serializers.JSONField()
    comment = serializers.CharField()
    post_id = serializers.CharField()


class ReadCommentSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField("get_type")
    author = serializers.SerializerMethodField("get_author")
    likes = serializers.SerializerMethodField("get_likes")
    id = serializers.SerializerMethodField("get_id")
    # post_id = serializers.SerializerMethodField('get_post_id')
    def get_type(self, obj):
        return "comment"

    def get_author(self, obj):
        return obj.author

    def get_likes(self, obj: Comment):
        return obj.likes.count()

    def get_id(self, obj: Comment):
        host = obj.author["id"]
        return f"{host}/posts/{obj.post_id}/comments/{obj.id}"

    class Meta:
        model = Comment
        fields = "__all__"


class LikeSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField("get_type")
    author = serializers.JSONField()
    object = serializers.URLField()

    def get_type(self, obj):
        return "like"

    class Meta:
        model = Like
        exclude = ("id", "is_comment", "published")


class ReadPostSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField("get_type")
    id = serializers.SerializerMethodField("get_id")
    title = serializers.CharField()
    source = serializers.CharField()
    origin = serializers.CharField()
    published = serializers.DateTimeField()
    description = serializers.CharField()
    unlisted = serializers.BooleanField()
    author = serializers.SerializerMethodField("get_author")
    visibility = serializers.CharField()
    contentType = serializers.CharField()
    content = serializers.SerializerMethodField("get_content")
    likes = serializers.SerializerMethodField("get_likes")
    count = serializers.SerializerMethodField("get_comments_count")
    commentsSrc = serializers.SerializerMethodField("get_comments_list")

    def get_author(self, model: Post):
        author = AuthorSerializer(model.author).data
        return author

    def get_id(self, model: Post):
        author_id = AuthorSerializer(model.author).data["id"]
        return f"{author_id}/posts/{model.id}"

    def get_type(self, model):
        return "post"

    def get_content(self, model: Post):
        if model.contentType in [
            "application/base64",
            "image/png;base64",
            "image/jpeg;base64",
        ]:
            return f"{self.get_id(model)}/image"
        else:
            return model.content

    def get_likes(self, model: Post):
        return model.likes.count()

    def get_comments_count(self, model: Post):
        return model.comments.count()

    def get_comments_list(self, model: Post):
        comments = model.comments.order_by("-published")[:5]
        return ReadCommentSerializer(comments, many=True).data

    class Meta:
        model = Post
        exclude = ("file",)


class ReadAuthorsPostsSerializer(serializers.Serializer):
    type = serializers.SerializerMethodField("get_type")
    items = serializers.SerializerMethodField("get_items")

    def get_type(self, _):
        return "posts"

    @extend_schema_field(serializers.ListSerializer(child=ReadPostSerializer()))
    def get_items(self, data):
        return data

    class Meta:
        fields = ("type", "items")


class AddInboxItemSerializer(serializers.ModelSerializer):
    item = serializers.JSONField()

    def create(self, validated_data, author_id):
        data = {"item": validated_data}
        inbox_item = InboxItem.objects.create(**data)
        author = Author.objects.get(id=author_id)
        inbox, _ = Inbox.objects.get_or_create(author=author)
        inbox.items.add(inbox_item)
        return inbox_item

    class Meta:
        model = InboxItem
        exclude = ["author"]


class ReadInboxSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField("get_type")
    items = serializers.SerializerMethodField("get_items")
    author = serializers.SerializerMethodField("get_author")

    def get_type(self, obj):
        return "inbox"

    def get_author(self, obj):
        return AuthorSerializer(obj["author"]).data.get("url")

    def get_items(self, obj) -> List:
        # Read the inbox items for the given author and convert them to the correct format
        items = []
        for item in obj["items"]:
            items.append(item.item)
        return items

    class Meta:
        model = Inbox
        fields = "__all__"

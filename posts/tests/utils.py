import base64
import json
from authors.models import Author

from posts.serializers import (
    CreatePostSerializer,
    CreateCommentSerializer
)


from django.test import TestCase
from django.test import TestCase


def create_author(display_name, email, password, username):
    return Author.objects.create(
        display_name=display_name,
        email=email,
        password=password,
        username=username,
    )


POST_DATA = {
    "title": "title",
    "source": "source",
    "origin": "origin",
    "description": "description",
    "unlisted": False,
    "visibility": "PUBLIC",
    "contentType": "text/plain",
    "content": "content",
}

POST_DATA_2 = {
    "title": "title",
    "source": "source",
    "origin": "origin",
    "description": "description",
    "unlisted": False,
    "visibility": "FRIENDS",
    "contentType": "text/plain",
    "content": "content",
}


def create_post(author, post_data=POST_DATA):
    return CreatePostSerializer().create(
        post_data.copy(),
        author.id,
    )

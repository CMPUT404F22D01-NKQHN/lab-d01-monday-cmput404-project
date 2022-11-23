INBOX_EXAMPLE = {
    "type": "inbox",
    "items": [
        {
            "id": "http://localhost:8000/authors/1c2b7d7b1edc400dac34be6f19310dd0/posts/3a7378d339134fcb8140b2edba79d008",
            "type": "post",
            "title": "title",
            "source": "source",
            "origin": "origin",
            "published": "2022-11-22T20:13:00.757232-07:00",
            "description": "description",
            "unlisted": False,
            "author": {
                "type": "author",
                "displayName": "test",
                "github": "",
                "host": "http://localhost:8000",
                "id": "http://localhost:8000/authors/1c2b7d7b1edc400dac34be6f19310dd0",
                "url": "http://localhost:8000/authors/1c2b7d7b1edc400dac34be6f19310dd0",
                "profileImage": "https://i.imgur.com/k7XVwpB.jpeg",
            },
            "visibility": "PUBLIC",
            "contentType": "text/plain",
            "content": "content",
            "likes": 0,
            "count": 0,
            "commentsSrc": [],
            "categories": [],
            "comments": [],
        }
    ],
    "author": "http://localhost:8000/authors/9dd577de5c8e4124be51e024853f9f22",
}


INBOX_ADD_FOLLOW_EXAMPLE = {
    "type": "inbox",
    "items": [
        {
            "id": "http://localhost:8000/authors/7b233c6cef03425d9e08d73ed7e89288/posts/d49aecea78134f4793d87b881b86d382/comments/3f4b3ce224704b74909c4c4d7837b4ae",
            "type": "comment",
            "author": {
                "type": "author",
                "displayName": "test2",
                "github": "",
                "host": "http://localhost:8000",
                "id": "http://localhost:8000/authors/7b233c6cef03425d9e08d73ed7e89288",
                "url": "http://localhost:8000/authors/7b233c6cef03425d9e08d73ed7e89288",
                "profileImage": "https://i.imgur.com/k7XVwpB.jpeg",
            },
            "likes": 0,
            "post_id": "d49aecea78134f4793d87b881b86d382",
            "comment": "test comment",
            "contentType": "text/plain",
            "published": "2022-11-22T20:17:02.883674-07:00",
        }
    ],
    "author": "http://localhost:8000/authors/578d8149c3744384bcc7dc0413f1d3ee",
}

INBOX_ADD_COMMENT_EXAMPLE = {
    "type": "comment",
    "post_id": "9919c7bf6f9e45678bd352e6da647485",
    "comment": "test comment",
    "author": {
        "type": "author",
        "displayName": "test2",
        "github": "",
        "host": "http://localhost:8000",
        "id": "http://localhost:8000/authors/570a510bbd434d7baae579d86db46067",
        "url": "http://localhost:8000/authors/570a510bbd434d7baae579d86db46067",
        "profileImage": "https://i.imgur.com/k7XVwpB.jpeg",
    },
}

INBOX_ADD_LIKE_EXAMPLE = {
    "summary": "Lara Croft Likes your post",
    "type": "like",
    "author": {
        "type": "author",
        "id": "http://127.0.0.1:5454/authors/9de17f29c12e8f97bcbbd34cc908f1baba40658e",
        "host": "http://127.0.0.1:5454/",
        "displayName": "Lara Croft",
        "url": "http://127.0.0.1:5454/authors/9de17f29c12e8f97bcbbd34cc908f1baba40658e",
        "github": "http://github.com/laracroft",
        "profileImage": "https://i.imgur.com/k7XVwpB.jpeg",
    },
    "object": "http://localhost:8000/authors/c221712d33284a50af2a4976a755d417/posts/e3219085711247f8b0bc3a8dc4550cd1",
}

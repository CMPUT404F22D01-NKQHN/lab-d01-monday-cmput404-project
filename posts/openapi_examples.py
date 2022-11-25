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
    "type": "follow",
    "summary": "Greg wants to follow Lara",
    "actor": {
        "type": "author",
        "id": "http://127.0.0.1:5454/authors/1d698d25ff008f7538453c120f581471",
        "url": "http://127.0.0.1:5454/authors/1d698d25ff008f7538453c120f581471",
        "host": "http://127.0.0.1:5454/",
        "displayName": "Greg Johnson",
        "github": "http://github.com/gjohnson",
        "profileImage": "https://i.imgur.com/k7XVwpB.jpeg",
    },
    "object": {
        "type": "author",
        "id": "http://127.0.0.1:5454/authors/9de17f29c12e8f97bcbbd34cc908f1baba40658e",
        "host": "http://127.0.0.1:5454/",
        "displayName": "Lara Croft",
        "url": "http://127.0.0.1:5454/authors/9de17f29c12e8f97bcbbd34cc908f1baba40658e",
        "github": "http://github.com/laracroft",
        "profileImage": "https://i.imgur.com/k7XVwpB.jpeg",
    },
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

LIKED_AUTHOR_EXAMPLE = [
    {
        "type": "like",
        "author": {
            "type": "author",
            "displayName": "test2",
            "github": "",
            "host": "http://localhost:8000",
            "id": "http://localhost:8000/authors/4d50cf79a15845368df7595f795920a9",
            "url": "http://localhost:8000/authors/4d50cf79a15845368df7595f795920a9",
            "profileImage": "https://i.imgur.com/k7XVwpB.jpeg"
        },
        "object": "http://localhost:8000/authors/4d50cf79a15845368df7595f795920a9/posts/e0af2eefb17043ef8a3cc9d8bba7cce2"
    },
    {
        "type": "like",
        "author": {
            "type": "author",
            "displayName": "sdds",
            "github": "rer",
            "host": "http://localhost:8000",
            "id": "http://localhost:8000/authors/4d50cf79a15845368df7595f795920a9",
            "url": "http://localhost:8000/authors/4d50cf79a15845368df7595f795920a9",
            "profileImage": "data:image/jpeg;base64,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",
            "uuid": "4d50cf79a15845368df7595f795920a9"
        },
        "object": "http://localhost:8000/authors/4d50cf79a15845368df7595f795920a9/posts/875ebe22abe046e0812cc8ce88259483/comments/abf79d494e564c9cad9b9aab365d905d"
    }]

LIKED_COMMENT_EXAMPLE = {
    "type": "liked",
    "items": [
        {
            "@context": "https://www.w3.org/ns/activitystreams",
            "summary": "Lara Croft Likes your comment",
            "type": "Like",
            "author": {
                "type": "author",
                "id": "http://127.0.0.1:5454/authors/9de17f29c12e8f97bcbbd34cc908f1baba40658e",
                "host": "http://127.0.0.1:5454/",
                "displayName": "Lara Croft",
                "url": "http://127.0.0.1:5454/authors/9de17f29c12e8f97bcbbd34cc908f1baba40658e",
                "github": "http://github.com/laracroft",
                "profileImage": "https://i.imgur.com/k7XVwpB.jpeg",
            },
            "object": "http://127.0.0.1:5454/authors/9de17f29c12e8f97bcbbd34cc908f1baba40658e/posts/764efa883dda1e11db47671c4a3bbd9e/comments/asd29832103asdbh12b3h21b3h12b3",
        }
    ],
}
POST_EXAMPLE = {
    "type": "post",
    "title": "A post title about a post about web dev",
    "id": "http://127.0.0.1:5454/authors/9de17f29c12e8f97bcbbd34cc908f1baba40658e/posts/764efa883dda1e11db47671c4a3bbd9e",
    "source": "http://lastplaceigotthisfrom.com/posts/yyyyy",
    "origin": "http://whereitcamefrom.com/posts/zzzzz",
    "description": "This post discusses stuff -- brief",
    "contentType": "text/plain",
    "content": "Þā wæs on burgum Bēowulf Scyldinga",
    "author": {
        "type": "author",
        "id": "http://127.0.0.1:5454/authors/9de17f29c12e8f97bcbbd34cc908f1baba40658e",
        "host": "http://127.0.0.1:5454/",
        "displayName": "Lara Croft",
        "url": "http://127.0.0.1:5454/authors/9de17f29c12e8f97bcbbd34cc908f1baba40658e",
        "github": "http://github.com/laracroft",
        "profileImage": "https://i.imgur.com/k7XVwpB.jpeg",
    },
    "categories": ["web", "tutorial"],
    "count": 1023,
    "comments": "http://127.0.0.1:5454/authors/9de17f29c12e8f97bcbbd34cc908f1baba40658e/posts/de305d54-75b4-431b-adb2-eb6b9e546013/comments/",
    "commentsSrc": {
        "type": "comments",
        "page": 1,
        "size": 5,
        "post": "http://127.0.0.1:5454/authors/9de17f29c12e8f97bcbbd34cc908f1baba40658e/posts/764efa883dda1e11db47671c4a3bbd9e",
        "id": "http://127.0.0.1:5454/authors/9de17f29c12e8f97bcbbd34cc908f1baba40658e/posts/de305d54-75b4-431b-adb2-eb6b9e546013/comments/",
        "comments": [
            {
                "type": "comment",
                "author": {
                    "type": "author",
                    # ID of the Author (UUID)
                    "id": "http://127.0.0.1:5454/authors/1d698d25ff008f7538453c120f581471",
                    # url to the authors information
                    "url": "http://127.0.0.1:5454/authors/1d698d25ff008f7538453c120f581471",
                    "host": "http://127.0.0.1:5454/",
                    "displayName": "Greg Johnson",
                    # HATEOS url for Github API
                    "github": "http://github.com/gjohnson",
                    # Image from a public domain
                    "profileImage": "https://i.imgur.com/k7XVwpB.jpeg",
                },
                "comment": "Sick Olde English",
                "contentType": "text/markdown",
                # ISO 8601 TIMESTAMP
                "published": "2015-03-09T13:07:04+00:00",
                # ID of the Comment (UUID)
                "id": "http://127.0.0.1:5454/authors/9de17f29c12e8f97bcbbd34cc908f1baba40658e/posts/de305d54-75b4-431b-adb2-eb6b9e546013/comments/f6255bb01c648fe967714d52a89e8e9c",
            }
        ],
    },
    "published": "2015-03-09T13:07:04+00:00",
    "visibility": "PUBLIC",
    "unlisted": "false",
}

POSTS_ADD_EXAMPLE = {
    "title": "A post title about a post about web dev",
    "source": "http://lastplaceigotthisfrom.com/posts/yyyyy",
    "origin": "http://whereitcamefrom.com/posts/zzzzz",
    "description": "This post discusses stuff -- brief",
    "contentType": "text/plain",
    "content": "Þā wæs on burgum Bēowulf Scyldinga",
    "visibility": "PUBLIC",
    "unlisted": "false",
}

SINGLE_COMMENT_EXAMPLE = {
    "type": "comment",
    "author": {
        "type": "author",
        # ID of the Author (UUID)
        "id": "http://127.0.0.1:5454/authors/1d698d25ff008f7538453c120f581471",
        # url to the authors information
        "url": "http://127.0.0.1:5454/authors/1d698d25ff008f7538453c120f581471",
        "host": "http://127.0.0.1:5454/",
        "displayName": "Greg Johnson",
        # HATEOS url for Github API
        "github": "http://github.com/gjohnson",
        # Image from a public domain
        "profileImage": "https://i.imgur.com/k7XVwpB.jpeg",
    },
    "comment": "Sick Olde English",
    "contentType": "text/markdown",
    # ISO 8601 TIMESTAMP
    "published": "2015-03-09T13:07:04+00:00",
    # ID of the Comment (UUID)
    "id": "http://127.0.0.1:5454/authors/9de17f29c12e8f97bcbbd34cc908f1baba40658e/posts/de305d54-75b4-431b-adb2-eb6b9e546013/comments/f6255bb01c648fe967714d52a89e8e9c",
}

POST_LIST_EXAMPLE = {
    "type": "posts",
    "items": [POST_EXAMPLE],
}

CREATE_COMMENT_EXAMPLE = {
    "comment": "Sick Olde English",
    "contentType": "text/markdown",
}
COMMENTS_EXAMPLE = {
    "type": "comments",
    "page": 1,
    "size": 5,
    "post": "http://127.0.0.1:5454/authors/9de17f29c12e8f97bcbbd34cc908f1baba40658e/posts/764efa883dda1e11db47671c4a3bbd9e",
    "id": "http://127.0.0.1:5454/authors/9de17f29c12e8f97bcbbd34cc908f1baba40658e/posts/de305d54-75b4-431b-adb2-eb6b9e546013/comments/",
    "comments": [
        {
            "type": "comment",
            "author": {
                "type": "author",
                # ID of the Author (UUID)
                "id": "http://127.0.0.1:5454/authors/1d698d25ff008f7538453c120f581471",
                # url to the authors information
                "url": "http://127.0.0.1:5454/authors/1d698d25ff008f7538453c120f581471",
                "host": "http://127.0.0.1:5454/",
                "displayName": "Greg Johnson",
                # HATEOS url for Github API
                "github": "http://github.com/gjohnson",
                # Image from a public domain
                "profileImage": "https://i.imgur.com/k7XVwpB.jpeg",
            },
            "comment": "Sick Olde English",
            "contentType": "text/markdown",
            # ISO 8601 TIMESTAMP
            "published": "2015-03-09T13:07:04+00:00",
            # ID of the Comment (UUID)
            "id": "http://127.0.0.1:5454/authors/9de17f29c12e8f97bcbbd34cc908f1baba40658e/posts/de305d54-75b4-431b-adb2-eb6b9e546013/comments/f6255bb01c648fe967714d52a89e8e9c",
        }
    ],
}

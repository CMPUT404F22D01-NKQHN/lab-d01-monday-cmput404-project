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

LIKED_AUTHOR_EXAMPLE = {
    "type":"liked",
    "items":[
        {
            "@context": "https://www.w3.org/ns/activitystreams",
            "summary": "Lara Croft Likes your post",         
            "type": "Like",
            "author":{
                "type":"author",
                "id":"http://127.0.0.1:5454/authors/9de17f29c12e8f97bcbbd34cc908f1baba40658e",
                "host":"http://127.0.0.1:5454/",
                "displayName":"Lara Croft",
                "url":"http://127.0.0.1:5454/authors/9de17f29c12e8f97bcbbd34cc908f1baba40658e",
                "github":"http://github.com/laracroft",
                "profileImage": "https://i.imgur.com/k7XVwpB.jpeg"
            },
            "object":"http://127.0.0.1:5454/authors/9de17f29c12e8f97bcbbd34cc908f1baba40658e/posts/764efa883dda1e11db47671c4a3bbd9e"
        }
    ]
}

LIKED_COMMENT_EXAMPLE = {
    "type":"liked",
    "items":[
        {
            "@context": "https://www.w3.org/ns/activitystreams",
            "summary": "Lara Croft Likes your comment",         
            "type": "Like",
            "author":{
                "type":"author",
                "id":"http://127.0.0.1:5454/authors/9de17f29c12e8f97bcbbd34cc908f1baba40658e",
                "host":"http://127.0.0.1:5454/",
                "displayName":"Lara Croft",
                "url":"http://127.0.0.1:5454/authors/9de17f29c12e8f97bcbbd34cc908f1baba40658e",
                "github":"http://github.com/laracroft",
                "profileImage": "https://i.imgur.com/k7XVwpB.jpeg"
            },
            "object":"http://127.0.0.1:5454/authors/9de17f29c12e8f97bcbbd34cc908f1baba40658e/posts/764efa883dda1e11db47671c4a3bbd9e/comments/asd29832103asdbh12b3h21b3h12b3"
        }
    ]
}

POST_EXAMPLE = {
    "type":"post",
    "title":"A post title about a post about web dev",
    "id":"http://127.0.0.1:5454/authors/9de17f29c12e8f97bcbbd34cc908f1baba40658e/posts/764efa883dda1e11db47671c4a3bbd9e",
    "source":"http://lastplaceigotthisfrom.com/posts/yyyyy",
    "origin":"http://whereitcamefrom.com/posts/zzzzz",
    "description":"This post discusses stuff -- brief",
    "contentType":"text/plain",
    "content":"Þā wæs on burgum Bēowulf Scyldinga",
    "author": { 
        "type":"author",
        "id":"http://127.0.0.1:5454/authors/9de17f29c12e8f97bcbbd34cc908f1baba40658e",
        "host":"http://127.0.0.1:5454/",
        "displayName":"Lara Croft",
        "url":"http://127.0.0.1:5454/authors/9de17f29c12e8f97bcbbd34cc908f1baba40658e",
        "github": "http://github.com/laracroft",
        "profileImage": "https://i.imgur.com/k7XVwpB.jpeg"
    },
    "categories":["web","tutorial"],
    "count": 1023,
    "comments":"http://127.0.0.1:5454/authors/9de17f29c12e8f97bcbbd34cc908f1baba40658e/posts/de305d54-75b4-431b-adb2-eb6b9e546013/comments",
    "commentsSrc":{
        "type":"comments",
        "page":1,
        "size":5,
        "post":"http://127.0.0.1:5454/authors/9de17f29c12e8f97bcbbd34cc908f1baba40658e/posts/764efa883dda1e11db47671c4a3bbd9e",
        "id":"http://127.0.0.1:5454/authors/9de17f29c12e8f97bcbbd34cc908f1baba40658e/posts/de305d54-75b4-431b-adb2-eb6b9e546013/comments",
        "comments":[
            {
                "type":"comment",
                "author":{
                    "type":"author",
                    # ID of the Author (UUID)
                    "id":"http://127.0.0.1:5454/authors/1d698d25ff008f7538453c120f581471",
                    # url to the authors information
                    "url":"http://127.0.0.1:5454/authors/1d698d25ff008f7538453c120f581471",
                    "host":"http://127.0.0.1:5454/",
                    "displayName":"Greg Johnson",
                    # HATEOS url for Github API
                    "github": "http://github.com/gjohnson",
                    # Image from a public domain
                    "profileImage": "https://i.imgur.com/k7XVwpB.jpeg"
                },
                "comment":"Sick Olde English",
                "contentType":"text/markdown",
                # ISO 8601 TIMESTAMP
                "published":"2015-03-09T13:07:04+00:00",
                # ID of the Comment (UUID)
                "id":"http://127.0.0.1:5454/authors/9de17f29c12e8f97bcbbd34cc908f1baba40658e/posts/de305d54-75b4-431b-adb2-eb6b9e546013/comments/f6255bb01c648fe967714d52a89e8e9c",
            }
        ]
    },
    "published":"2015-03-09T13:07:04+00:00",
    "visibility":"PUBLIC",
    "unlisted":"false"
}

POSTS_ADD_EXAMPLE = {
    "type":"post",
    "title":"A post title about a post about web dev",
    "id":"http://127.0.0.1:5454/authors/9de17f29c12e8f97bcbbd34cc908f1baba40658e/posts/764efa883dda1e11db47671c4a3bbd9e",
    "source":"http://lastplaceigotthisfrom.com/posts/yyyyy",
    "origin":"http://whereitcamefrom.com/posts/zzzzz",
    "description":"This post discusses stuff -- brief",
    "contentType":"text/plain",
    "content":"Þā wæs on burgum Bēowulf Scyldinga",
    "author": { 
        "type":"author",
        "id":"http://127.0.0.1:5454/authors/9de17f29c12e8f97bcbbd34cc908f1baba40658e",
        "host":"http://127.0.0.1:5454/",
        "displayName":"Lara Croft",
        "url":"http://127.0.0.1:5454/authors/9de17f29c12e8f97bcbbd34cc908f1baba40658e",
        "github": "http://github.com/laracroft",
        "profileImage": "https://i.imgur.com/k7XVwpB.jpeg"
    },
    "categories":["web","tutorial"],
    "count": 1023,
    "comments":"http://127.0.0.1:5454/authors/9de17f29c12e8f97bcbbd34cc908f1baba40658e/posts/de305d54-75b4-431b-adb2-eb6b9e546013/comments",
    "commentsSrc":{},
    "published":"2015-03-09T13:07:04+00:00",
    "visibility":"PUBLIC",
    "unlisted":"false"
}

SINGLE_COMMENT_EXAMPLE = {
    "type":"comment",
    "author":{
        "type":"author",
        # ID of the Author (UUID)
        "id":"http://127.0.0.1:5454/authors/1d698d25ff008f7538453c120f581471",
        # url to the authors information
        "url":"http://127.0.0.1:5454/authors/1d698d25ff008f7538453c120f581471",
        "host":"http://127.0.0.1:5454/",
        "displayName":"Greg Johnson",
        # HATEOS url for Github API
        "github": "http://github.com/gjohnson",
        # Image from a public domain
        "profileImage": "https://i.imgur.com/k7XVwpB.jpeg"
    },
    "comment":"Sick Olde English",
    "contentType":"text/markdown",
    # ISO 8601 TIMESTAMP
    "published":"2015-03-09T13:07:04+00:00",
    # ID of the Comment (UUID)
    "id":"http://127.0.0.1:5454/authors/9de17f29c12e8f97bcbbd34cc908f1baba40658e/posts/de305d54-75b4-431b-adb2-eb6b9e546013/comments/f6255bb01c648fe967714d52a89e8e9c",
}

COMMENTS_EXAMPLE = {
    "type":"comments",
    "page":1,
    "size":5,
    "post":"http://127.0.0.1:5454/authors/9de17f29c12e8f97bcbbd34cc908f1baba40658e/posts/764efa883dda1e11db47671c4a3bbd9e",
    "id":"http://127.0.0.1:5454/authors/9de17f29c12e8f97bcbbd34cc908f1baba40658e/posts/de305d54-75b4-431b-adb2-eb6b9e546013/comments",
    "comments":[
        {
            "type":"comment",
            "author":{
                "type":"author",
                # ID of the Author (UUID)
                "id":"http://127.0.0.1:5454/authors/1d698d25ff008f7538453c120f581471",
                # url to the authors information
                "url":"http://127.0.0.1:5454/authors/1d698d25ff008f7538453c120f581471",
                "host":"http://127.0.0.1:5454/",
                "displayName":"Greg Johnson",
                # HATEOS url for Github API
                "github": "http://github.com/gjohnson",
                # Image from a public domain
                "profileImage": "https://i.imgur.com/k7XVwpB.jpeg"
            },
            "comment":"Sick Olde English",
            "contentType":"text/markdown",
            # ISO 8601 TIMESTAMP
            "published":"2015-03-09T13:07:04+00:00",
            # ID of the Comment (UUID)
            "id":"http://127.0.0.1:5454/authors/9de17f29c12e8f97bcbbd34cc908f1baba40658e/posts/de305d54-75b4-431b-adb2-eb6b9e546013/comments/f6255bb01c648fe967714d52a89e8e9c",
        }
    ]
}
      
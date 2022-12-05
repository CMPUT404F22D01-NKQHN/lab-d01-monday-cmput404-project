import base64
import json
from rest_framework.response import Response

from authors.models import Author
from cmput404_project.utilities import CustomPagination, gen_id
from friends.serializers import FriendRequestSerializer
from posts.openapi_examples import *
from .models import Inbox, Like, Post, Comment
from .serializers import (
    AddInboxItemSerializer,
    CommentInboxItemSerializer,
    ReadInboxSerializer,
    LikeSerializer,
)
from nodes.models import Node
from rest_framework.generics import GenericAPIView
import requests
from drf_spectacular.utils import extend_schema, OpenApiExample


def handle_comment_inbox(request):
    # print("comment")
    # TODO: Check if the comment is valid
    # If it is, add it to the post too
    post = None
    comment = None
    parsed_id = request.data["object"].split("/")[-1]
    try:
        post = Post.objects.get(id=parsed_id)
    except Post.DoesNotExist:
        return Response(
            status=404,
            data={"error": "The post you are commenting on does not exist."},
        )
    try:
        # Check if the comment is valid
        validated_data = CommentInboxItemSerializer(data=request.data)
        validated_data.is_valid(raise_exception=True)
        comment = Comment.objects.create(
            author=request.data["author"],
            comment=request.data["comment"],
            contentType=request.data.get("contentType", "text/plain"),
            post_id=post.id,
        )
    except Exception as e:
        print(e)
        return Response(
            status=400,
            data={"error": "The comment you are trying to add is invalid."},
        )
    post.comments.add(comment)
    post.save()


class InboxAPIView(GenericAPIView):
    
    
    def get_serializer_class(self):
        if self.request.method == "POST":
            return AddInboxItemSerializer
        elif self.request.method == "DELETE":
            return None
        return ReadInboxSerializer
    
    @extend_schema(
        responses=ReadInboxSerializer,
        examples=[
            OpenApiExample(
                "Inbox",
                value=INBOX_EXAMPLE,
            )
        ],
        description="Get the inbox of the current user",
    )
    def get(self, request, author_id):
        try:
            author = Author.objects.get(id=author_id)
            assert author.id == request.user.id
            inbox, _ = Inbox.objects.get_or_create(author=author)
            items = self.paginate_queryset(
                inbox.items.order_by("-published").all(), request
            )
            obj = {
                "items": items,
                "author": author,
            }
            return Response(ReadInboxSerializer(obj).data)
        except AssertionError:
            return Response(
                status=403, data={"error": "You are not authorized to view this page."}
            )

    def paginate_queryset(self, queryset, request):
        return self.pagination_class().paginate_queryset(queryset, request, view=self)

    pagination_class = CustomPagination

    @extend_schema(
        responses=str,
        examples=[
            OpenApiExample(
                "Follower example",
                value=INBOX_ADD_FOLLOW_EXAMPLE,
                request_only=True,
            ),
            OpenApiExample(
                "Like example",
                value=INBOX_ADD_LIKE_EXAMPLE,
                request_only=True,
            ),
            OpenApiExample(
                "Comment example",
                value=INBOX_ADD_COMMENT_EXAMPLE,
                request_only=True,
            ),
        ],
        description="Add an item to the inbox of the current user",
    )
    def post(self, request, author_id):
        try:
            author = None
            try:
                author = Author.objects.get(id=author_id)
            except Author.DoesNotExist:
                # Check if author exists on remote server
                for node in Node.objects.all():
                    try:
                        author = requests.get(
                            f"{node.api_url}authors/{author_id}"
                        ).json()
                        assert author["host"] in node.api_url
                        response = requests.get(
                            f"{node.api_url}authors/{author_id}")
                        print("Checking remote server",f"{node.api_url}authors/{author_id}")
                        if response.status_code == 200:
                            author = Author.objects.create(
                                id=author_id,
                                host=node.api_url,
                                display_name=response.json()["displayName"],
                                proxy=True,
                                username=gen_id()
                            )
                            node.proxy_users.add(author)
                            break
                    except Exception as e:
                        print(e)
                        continue
            if not author:
                return Response(
                    status=404,
                    data={"error": "The author you are trying to add does not exist."},
                )
            if Node.objects.filter(proxy_users=author).exists():
                print("proxy user")
                node = Node.objects.get(proxy_users=author)
                api_url = node.api_url + "authors/" + author_id + "/inbox/"
                print("URL",api_url)
                creds = base64.b64encode(f"{node.username}:{node.password}".encode()).decode()
                response = requests.post(
                    api_url,
                    data=json.dumps(request.data),
                    headers={"Authorization": f"basic {creds}", "Content-Type": "application/json"},
                )
                print(response.status_code)
                print(response.text)
                print(json.dumps(request.data))
                return Response(response.json(), status=response.status_code)
            if request.user.is_another_server:
                """
                This block of code is essentially to handle post requests from other servers
                The assumption is that since the request contains information about the author,
                we can create a proxy user for that author.

                We can use this proxy user to send outgoing inbox messages.
                """
                if "author" not in request.data and "actor" not in request.data:
                    return Response(
                        status=400,
                        data={
                            "error": "The author/actor field is required for this request."
                        },
                    )
                author_obj = request.data.get("author", request.data.get("actor"))
                    
                foreign_author_id = author_obj["id"].split("/")[-1]
                if not Author.objects.filter(id=foreign_author_id).exists():
                    print("Author does not exist, creating proxy user")
                    foreign_author, _ = Author.objects.get_or_create(
                        id=foreign_author_id,
                        host=author_obj["host"],
                        display_name=author_obj["displayName"],
                        proxy=True,
                        username=gen_id()
                    )
                    # Add foreign author to the proxy users field in the node
                    node = Node.objects.get(team_account=request.user)
                    node.proxy_users.add(foreign_author)
            if request.data["type"].lower() == "comment":
                res = handle_comment_inbox(request)
                if res:
                    return res

            elif (
                request.data["type"].lower() == "like"
                and LikeSerializer(data=request.data).is_valid()
            ):
                # print("like")
                # TODO: Check if the like is valid
                # If it is, add it to the post or comment
                post = None
                comment = None
                parsed_id = request.data["object"].split("/")[-1]
                if "comment" in request.data["object"]:
                    try:
                        comment = Comment.objects.get(id=parsed_id)
                    except Comment.DoesNotExist:
                        return Response(
                            status=404,
                            data={
                                "error": "The comment you are liking does not exist."
                            },
                        )
                    like = Like.objects.create(
                        author=request.data["author"],
                        object=request.data["object"],
                        is_comment=True,
                    )
                    comment.likes.add(like)
                    comment.save()
                else:
                    try:
                        post = Post.objects.get(id=parsed_id)
                    except Post.DoesNotExist:
                        return Response(
                            status=404,
                            data={"error": "The post you are liking does not exist."},
                        )
                    like = Like.objects.create(
                        author=request.data["author"],
                        object=request.data["object"],
                        is_comment=False,
                    )
                    post.likes.add(like)
                    post.save()
                # If author is on local server, add to that author's liked list
                liker_id = request.data["author"]["id"].split("/")[-1]
                try:
                    liker = Author.objects.get(id=liker_id)
                    liker.liked.add(like)
                    liker.save()
                except Author.DoesNotExist:
                    pass

            elif request.data["type"].lower() == "post":
                # print("post")
                pass
                # TODO: Check if the post is valid

            elif request.data["type"].lower() == "follow":
                # TODO: Check if the friend request is valid
                req = FriendRequestSerializer(data=request.data)
                req.is_valid()
                if not req.is_valid():
                    return Response(
                        status=400,
                        data={"error": req.errors},
                    )

            else:
                return Response(status=400, data={"error": "Invalid item type."})

            author = Author.objects.get(id=author_id)
            AddInboxItemSerializer().create(request.data, author.id)
            return Response("Success", status=201)
        except Exception as e:
            print(e)
            return Response(
                status=500, data={"error": "Something went wrong. Please try again."}
            )

    def delete(self, request, author_id):
        """
        Clear all content from the inbox
        """
        try:
            author = Author.objects.get(id=author_id)
            assert author.id == request.user.id
            inbox, _ = Inbox.objects.get_or_create(author=author)
            inbox.items.all().delete()
            obj = {
                "items": inbox.items.order_by("-published").all(),
                "author": author,
            }
            return Response(ReadInboxSerializer(obj).data)
        except AssertionError:
            return Response(
                status=403, data={"error": "You are not authorized to view this page."}
            )

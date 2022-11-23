from rest_framework.response import Response

from authors.models import Author
from cmput404_project.utilities import CustomPagination
from friends.serializers import FriendRequestSerializer
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


def handle_comment_inbox(request):
    # print("comment")
    # TODO: Check if the comment is valid
    # If it is, add it to the post too
    post = None
    comment = None
    parsed_id = request.data["post_id"].split("/")[-1]
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
        return Response(
            status=400,
            data={"error": "The comment you are trying to add is invalid."},
        )
    post.comments.add(comment)
    post.save()


class InboxAPIView(GenericAPIView):
    def get_serializer_class(self):
        if self.request.method == "GET":
            return ReadInboxSerializer
        elif self.request.method == "POST":
            return AddInboxItemSerializer
        return ReadInboxSerializer

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

    def post(self, request, author_id):
        try:
            author = Author.objects.get(id=author_id)
            if Node.objects.filter(proxy_users=author).exists():
                print("proxy user")
                node = Node.objects.get(proxy_users=author)
                api_url = node.url + "author/" + author_id + "/inbox/"
                response = requests.post(
                    api_url,
                    data=request.data,
                    content_type="application/json",
                    headers={"Authorization": f"Basic {node.username}:{node.password}"},
                )
                return Response(response.json(), status=response.status_code)
            if request.user.is_another_server:
                """
                This block of code is essentially to handle post requests from other servers
                The assumption is that since the request contains information about the author,
                we can create a proxy user for that author.

                We can use this proxy user to send outgoing inbox messages.
                """
                if "author" not in request.data:
                    return Response(
                        status=400,
                        data={
                            "error": "The author field is required for this request."
                        },
                    )
                foreign_author_id = request.data["author"]["id"].split("/")[-1]
                if not Author.objects.filter(id=foreign_author_id).exists():
                    print("Author does not exist, creating proxy user")
                    auth_obj = request.data["author"]
                    foreign_author, _ = Author.objects.get_or_create(
                        id=foreign_author_id,
                        host=auth_obj["host"],
                        display_name=auth_obj["displayName"],
                    )
                    # Add foreign author to the proxy users field in the node
                    node = Node.objects.get(team_account=request.user)
                    node.proxy_users.add(foreign_author)
            if request.data["type"] == "comment":
                handle_comment_inbox(request)

            elif (
                request.data["type"] == "like"
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

            elif request.data["type"] == "post":
                # print("post")
                pass
                # TODO: Check if the post is valid

            elif request.data["type"] == "follow":
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

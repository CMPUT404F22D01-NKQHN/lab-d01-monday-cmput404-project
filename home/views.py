from django.shortcuts import render
from authors.models import Author
from authors.serializers import AuthorSerializer
from datetime import datetime
import requests
from django.contrib.auth.decorators import login_required
from authors import serializers
from django.http import HttpResponse

from django.shortcuts import redirect

# Create your views here.
import json


def login(request):
    return render(request, "login.html")


# I think here we will send all the required data for the feed as well as the buttons for the user to click on i.e. posts
@login_required(login_url="/login")
def home(request):
    authors = requests.get(request.build_absolute_uri("/authors/"))
    all_posts = []
    for link in authors.json()["items"]:
        try:
            author_posts = requests.get(link["id"] + "/posts/")

            print(author_posts)
            # get each pot from every author and add to posts
            for post in author_posts.json()["items"]:
                all_posts.append(post)
        except:
            pass

    # sort posts newest to oldest
    sorted_posts = sorted(
        all_posts,
        key=lambda x: datetime.strptime(x["published"], "%Y-%m-%dT%H:%M:%S.%f%z"),
    )
    sorted_posts.reverse()
    context = {
        "author_list": sorted_posts,
        "author_id": AuthorSerializer(request.user).data["id"],
        "title": "Home",
    }
    # Not context
    return render(request, "home/index.html", context)


@login_required(login_url="/login/")
def profile(request):
    author = Author.objects.all()
    x = AuthorSerializer(request.user).data
    print(x)
    author_id = request.user.id
    cookies = "; ".join([f"{key}={value}" for key, value in request.COOKIES.items()])
    posts = requests.get(
        request.build_absolute_uri("/authors/" + str(author_id) + "/posts/"),
        headers={
            "Content-Type": "application/json",
            "X-CSRFToken": request.COOKIES["csrftoken"],
            "Cookie": cookies,
        },
    )
    print(posts)
    # print(posts.json())
    # Get authors posts from post.json().items() using a for loop
    # for key, value in posts.json().items():
    #     print(key, value)

    # author_posts =
    # for item in posts.json()["items"]:
    #     print(item["author"])

    # author_posts = posts.json()["items"]
    # convert author_posts to a dict indexable by numbers
    # change dict key to be ordered by published date

    # loop through each post
    author_posts = posts.json().get("items", [])

    # sort posts newest to oldest
    sorted_posts = sorted(
        author_posts,
        key=lambda x: datetime.strptime(x["published"], "%Y-%m-%dT%H:%M:%S.%f%z"),
    )
    sorted_posts.reverse()
    # print(sorted_posts)

    # author = requests.get(request.build_absolute_uri('/authors/'+str(author_id)))
    # print("USER:", author.json())
    # print("USER:", serializers.AuthorSerializer(request.user).data)

    context = {
        "author_list": sorted_posts,
        "author_id": AuthorSerializer(request.user).data["id"],
        "title": "Profile",
    }

    # author_posts = dict(enumerate((posts.json()["items"][0])["author"]))
    # print(context)
    # print(posts.json().items())
    # author_github = Author.github
    # author_profileImage = Author.profileImage
    # author_is_admin = Author.is_admin
    # author_REQUIRED_FIELDS = Author.REQUIRED_FIELDS
    # author_followers = Author.followers

    return render(request, "profile/profile.html", context)


# view for author inbox
# {
#     "type": "inbox",
#     "items": [],
#     "author": "http://localhost:8000/authors/{AUTHOR_ID}}"
# }
@login_required(login_url="/login/")
def inbox(request):
    author = Author.objects.all()
    author_id = request.user.id
    print(author_id)
    # simulating forwarding all cookies on authenticated webview and passing them forward (could be problematic)
    cookies = "; ".join([f"{key}={value}" for key, value in request.COOKIES.items()])
    inboxItems = requests.get(
        request.build_absolute_uri("/authors/" + str(author_id) + "/inbox/"),
        headers={
            "Content-Type": "application/json",
            "X-CSRFToken": request.COOKIES["csrftoken"],
            "Cookie": cookies,
        },
    )

    print("URL", request.build_absolute_uri("/authors/" + str(author_id) + "/inbox/"))
    author_inbox = []
    for item in inboxItems.json()["items"]:
        if "author" in item:
            item["author"]["uuid"] = item["author"]["id"].split("/")[-1]
        if "actor" in item:
            item["actor"]["uuid"] = item["actor"]["id"].split("/")[-1]
        author_inbox.append(item)

    print(author_inbox)
    # default page size is 5 and give option to change pages
    context = {
        "author_inbox": author_inbox,
        "inbox_url": "/authors/" + str(author_id) + "/inbox/",
    }
    return render(request, "inbox/inbox.html", context)


@login_required(login_url="/login/")
def followers(request):
    server_opts = (
        requests.get(request.build_absolute_uri("/nodes/")).json().get("nodes", [])
    )
    servers = {server["nickname"]: server["api_url"] for server in server_opts}
    # If no page query param or if page and size are not integers, redirect to page 1
    if (
        "page" not in request.GET
        or "size" not in request.GET
        or not request.GET["page"].isdigit()
        or not request.GET["size"].isdigit()
    ):
        return redirect("/followers?page=1&size=5")
    page = int(request.GET.get("page"))
    size = int(request.GET.get("size"))

    server = request.GET.get("server", "local")
    if server not in servers and server != "local":
        server = "local"
        return redirect(f"/followers?page={page}&size={size}&server={server}")
    servers["local"] = request.build_absolute_uri("/")
    authors_res = requests.get(
        servers[server] + "authors/?page=" + str(page) + "&size=" + str(size)
    )
    try:
        authors_res = authors_res.json()
        assert "items" in authors_res
    except:
        print("Error: ", authors_res)
        authors_res = {}
    all_users = authors_res.get("items", [])
    author_followers = requests.get(
        request.build_absolute_uri("/authors/" + str(request.user.id) + "/followers")
    ).json()["items"]
    for user in all_users:
        user["uuid"] = user["id"].split("/")[-1]
    for user in author_followers:
        user["uuid"] = user["id"].split("/")[-1]
    context = {
        "all_users": all_users,
        "author_followers": author_followers,
        "author_url": serializers.AuthorSerializer(request.user).data["id"],
        "page": page,
        "size": size,
        "server": server,
        "server_opts": [{"nickname": k, "api_url": v} for k, v in servers.items()],
    }

    return render(request, "followers/index.html", context)


def user(request, author_id):
    server = request.GET.get("server", "local")
    server_opts = (
        requests.get(request.build_absolute_uri("/nodes/")).json().get("nodes", [])
    )
    servers = {server["nickname"]: server["api_url"] for server in server_opts}
    servers["local"] = request.build_absolute_uri("/")
    selected_server = servers.get(server, None)
    if selected_server is None:
        return HttpResponse("Invalid server", status=400)
    try:
        user_info = requests.get(
            request.build_absolute_uri(selected_server + "authors/" + str(author_id))
        ).json()
        if user_info.get("host") != request.build_absolute_uri("/"):
            print("Redirecting to", user_info.get("host"))
            raise Exception("User not found")
    except:
        found = False
        for server in servers.values():
            try:
                user_info = requests.get(
                    request.build_absolute_uri(server + "authors/" + str(author_id))
                ).json()
                selected_server = server
                found = True
                break
            except:
                continue
        if not found:
            return HttpResponse("User not found", status=404)
    authors_posts = []
    try:
        authors_posts = requests.get(
            request.build_absolute_uri(
                selected_server + "authors/" + str(author_id) + "/posts/")).json()["items"]
        
    except:
        pass
    
    user_info["uuid"] = user_info["id"].split("/")[-1]
    
    is_follower = request.user.followers.filter(id=author_id).exists()

    return render(
        request,
        "user/index.html",
        {
            "user_info": user_info,
            "author_id": AuthorSerializer(request.user).data["id"],
            "is_follower": is_follower,
            "authors_posts": authors_posts,
        },
    )

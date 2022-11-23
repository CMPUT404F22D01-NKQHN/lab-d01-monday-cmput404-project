from django.shortcuts import render
from authors.models import Author
from authors.serializers import AuthorSerializer
from datetime import datetime
import requests
from django.contrib.auth.decorators import login_required
from authors import serializers
from django.http import HttpResponse

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
        author_posts = requests.get(link["id"] + "/posts")

        print(author_posts)
        # get each pot from every author and add to posts
        for post in author_posts.json()["items"]:
            all_posts.append(post)

    # sort posts newest to oldest
    sorted_posts = sorted(
        all_posts,
        key=lambda x: datetime.strptime(x["published"], "%Y-%m-%dT%H:%M:%S.%f%z"),
    )
    sorted_posts.reverse()
    context = {
        "author_list": sorted_posts,
        "author_id": request.user.id,
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
        request.build_absolute_uri("/authors/" + str(author_id) + "/posts"),
        headers={"Content-Type": "application/json", "X-CSRFToken": request.COOKIES["csrftoken"],
            "Cookie": cookies},
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
    author_posts = []
    for item in posts.json()["items"]:
        # bring all of the author attributes into a dictionary combined with the post attributes
        temp_dict = {}

        # add everything except the author attributes
        for key, value in item.items():
            if key == "author":
                # add everything from the author attributes except type
                for subkey, subvalue in value.items():
                    if subkey == "id":
                        temp_dict["post_id"] = subvalue
                    elif subkey != "type":
                        temp_dict[subkey] = subvalue
            else:
                temp_dict[key] = value

        # add new combined post + author attributes to list of posts
        author_posts.append(temp_dict)

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
        request.build_absolute_uri("/authors/" + str(author_id) + "/inbox"),
        headers={
            "Content-Type": "application/json",
            "X-CSRFToken": request.COOKIES["csrftoken"],
            "Cookie": cookies,
        },
    )

    print("URL", request.build_absolute_uri("/authors/" + str(author_id) + "/inbox"))
    author_inbox = []
    for item in inboxItems.json()["items"]:
        temp_dict = {}
        # if item["unlisted"] == "false":
        #     temp_dict["displayName"] = item["author"]["displayName"]
        for k, v in item.items():
            if k != "author":
                temp_dict[k] = v
        author_inbox.append(temp_dict)

    print(author_inbox)
    # default page size is 5 and give option to change pages
    context = {"author_inbox": author_inbox}
    return render(request, "inbox/inbox.html", context)


@login_required(login_url="/login/")
def followers(request):
    page = int(request.GET.get("page", 1))
    size = int(request.GET.get("size", 5))
    all_users = requests.get(
        request.build_absolute_uri("/authors/?page=" + str(page) + "&size=" + str(size))
    ).json()["items"]
    author_followers = requests.get(
        request.build_absolute_uri("/authors/" + str(request.user.id) + "/followers")
    ).json()["items"]
    context = {
        "all_users": all_users,
        "author_followers": author_followers,
        "author_url": serializers.AuthorSerializer(request.user).data["id"],
    }

    return render(request, "followers/index.html", context)

def user(request, author_id):
    try:
        user_info = requests.get(
            request.build_absolute_uri("/authors/" + str(author_id))
        ).json()
    except:
        return HttpResponse(status=404)
    
    is_follower = request.user.followers.filter(id=author_id).exists()
    
    
    
    return render(request, "user/index.html", {"user_info": user_info, "author_id": AuthorSerializer(request.user).data["id"], "is_follower": is_follower})
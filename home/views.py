import re
from django.shortcuts import render
from authors.models import Author
from posts.models import Post
from datetime import datetime
import requests
import json
# Create your views here.

# I think here we will send all the required data for the feed as well as the buttons for the user to click on i.e. posts

def home(request):
    
    #authors = Author.objects.all()
    # We need to be sending authors2 

    # get all author id's
    authors = requests.get('http://localhost:8000/authors')
    all_posts = []
    for link in authors.json()["items"]:
        author_posts = requests.get(link["id"] + '/posts')

        print(author_posts)
        for post in author_posts.json()["items"]:
            all_posts.append(post)
    
    # sort posts newest to oldest
    sorted_posts = sorted(all_posts, key =lambda x: datetime.strptime(x["published"][:-12], "%Y-%m-%dT%H:%M:%S."))
    sorted_posts.reverse()
    print(sorted_posts)

    # Get posts and order by published date
    posts = Post.objects.all().order_by('-published')
    # get the posts title and author
    #posts = posts.values('title', 'author', 'id', 'published')
    context = {
        "author_list" : sorted_posts
    }
    # Not context
    return render(request, 'home/index.html', context)

def profile(request):
    author = Author.objects.all()
    author_id = int(request.user.id)
    posts = requests.get('http://localhost:8000/authors/'+str(author_id)+'/posts')
    # Get authors posts from post.json().items() using a for loop    
    # for key, value in posts.json().items():
    #     print(key, value)


    #author_posts = 
    # for item in posts.json()["items"]:
    #     print(item["author"])

    #author_posts = posts.json()["items"]
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
                    if key != "type":
                        temp_dict[subkey] = subvalue
            else:
                temp_dict[key] = value

        # add new combined post + author attributes to list of posts
        author_posts.append(temp_dict)
    
    # print(author_posts)

    context = {
        "author_list" : author_posts
    }

    # author_posts = dict(enumerate((posts.json()["items"][0])["author"]))
    #print(context)
    #print(posts.json().items())
    # author_github = Author.github
    # author_profileImage = Author.profileImage
    # author_is_admin = Author.is_admin
    # author_REQUIRED_FIELDS = Author.REQUIRED_FIELDS
    # author_followers = Author.followers

    
    return render(request, 'profile/profile.html', context)
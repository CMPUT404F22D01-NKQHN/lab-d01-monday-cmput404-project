from django.shortcuts import render
from authors.models import Author
from posts.models import Post
import requests
# Create your views here.

# I think here we will send all the required data for the feed as well as the buttons for the user to click on i.e. posts

def home(request):
    
    authors = Author.objects.all()
    # We need to be sending authors2 
    authors2 = requests.get('http://127.0.0.1:8000/authors')
    print(authors2.json())
    # Get posts and order by published date
    posts = Post.objects.all().order_by('-published')
    # get the posts title and author
    #posts = posts.values('title', 'author', 'id', 'published')
    context = {
        'posts': posts,
        'authors': authors,
        'author_id': int(request.user.id),
    }
    # Not context 
    return render(request, 'home/index.html', context)

def profile(request):
    
    author = Author.objects.all()
    # author_github = Author.github
    # author_profileImage = Author.profileImage
    # author_is_admin = Author.is_admin
    # author_REQUIRED_FIELDS = Author.REQUIRED_FIELDS
    # author_followers = Author.followers

    context = {
        'author': author,
        # 'author_github': author_github,
        # 'author_profileImage': author_profileImage,
        # 'author_is_admin': author_is_admin, 
        # 'author_REQUIRED_FIELDS': author_REQUIRED_FIELDS, 
        # 'author_followers': author_followers, 
    }
    
    return render(request, 'profile/profile.html', context)
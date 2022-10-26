from django.shortcuts import render
from authors.models import Author
from posts.models import Post
# Create your views here.

# I think here we will send all the required data for the feed as well as the buttons for the user to click on i.e. posts

def home(request):
    
    authors = Author.objects.all()
    # Get posts and order by published date
    posts = Post.objects.all().order_by('-published')
    # get the posts title and author
    #posts = posts.values('title', 'author', 'id', 'published')
    context = {
        'posts': posts,
        'authors': authors
    }
    
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
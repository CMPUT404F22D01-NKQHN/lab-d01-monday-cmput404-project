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
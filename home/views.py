from django.shortcuts import render
from authors.models import Author
from posts.models import Post
# Create your views here.

# This is where the home page will be rendered obviously still need to add the html file
def home(request):
    
    authors = Author.objects.all()
    # Get posts and order by published date
    posts = Post.objects.all().order_by('-published')
    # get the posts title and author
    posts = posts.values('title', 'author')
    context = {
        'posts': posts,
        'authors': authors
    }
    
    return render(request, 'home/index.html', context)
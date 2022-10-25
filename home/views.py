from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def home(request):
    # This is where the home page will be rendered obviously still need to add the html file
    return HttpResponse("Hello, world. You're at the home page.")
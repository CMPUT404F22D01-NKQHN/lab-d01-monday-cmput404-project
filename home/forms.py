#https://www.javatpoint.com/django-usercreationform#:~:text=Django%20UserCreationForm%20is%20used%20for,contrib.
from django import forms  
from django.contrib.auth.models import User  
from django.contrib.auth.forms import UserCreationForm  
from django.core.exceptions import ValidationError  
from django.forms.fields import EmailField  
from django.forms.forms import Form

class UserLoginForm(UserCreationForm):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    

    class Meta(UserCreationForm.Meta):
        model = User
        # I've tried both of these 'fields' declaration, result is the same
        # fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email',)
        
# This will be to post a form
class PostForm(Form):
    pass
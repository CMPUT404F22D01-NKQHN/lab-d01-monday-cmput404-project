from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
import uuid
# Create your models here.

class AuthorManager(BaseUserManager):
    def create_user(self, email: str, display_name, password, **kwargs):
        if not password:
            raise ValueError("Authors must enter a valid password")
        if not email:
            raise ValueError("Authors must enter a valid email address")

        email = self.normalize_email(email)
        user = self.model(email = email, display_name = display_name, password = password, **kwargs)
        user.set_password(password)
        user.is_admin = True
        user.save()
        return user


    def create_superuser(self, email: str, display_name, password, **kwargs):
        if not password:
            raise ValueError("Authors must enter a valid password")
        if not email:
            raise ValueError("Authors must enter a valid email address")

        email = self.normalize_email(email)
        user = self.model(email = email, display_name = display_name, password = password, **kwargs)
        user.set_password(password)
        user.is_admin = True
        user.save()
        return user



class Author(AbstractUser):
    #email = models.EmailField(verbose_name = 'email', max_length = 200, unique = True)
    id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False) 
    # url = models.TextField(max_length=100, blank= False, editable = False)
    # host = models.TextField(max_length=200, default = 'localhost')
    display_name = models.TextField(max_length=200, editable = True)
    github = models.TextField(max_length = 200, default = '', blank = True)
    #profileImage = models.ImageField(blank = True)
    is_admin = models.BooleanField(default=True)
    REQUIRED_FIELDS = ['email', 'display_name', 'password']

    objects = AuthorManager()
    
    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin



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
        user.is_admin = False
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
    id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False) 
    display_name = models.TextField(max_length=200, editable = True)
    github = models.TextField(max_length = 200, default = '', blank = True)
    profileImage = models.TextField(max_length = 200, default = '', blank = True)
    is_admin = models.BooleanField(default=False)
    REQUIRED_FIELDS = ['email', 'display_name', 'password']
    followers = models.ManyToManyField('Author')
    objects = AuthorManager()
    def __str__(self):
        return self.display_name   

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True
    
    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin



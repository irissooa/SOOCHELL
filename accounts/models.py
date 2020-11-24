from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from movies.models import Genre

# Create your models here.
class User(AbstractUser):
    genre = models.ManyToManyField(Genre, related_name="user")

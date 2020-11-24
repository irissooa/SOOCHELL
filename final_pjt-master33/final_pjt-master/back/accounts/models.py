from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from movies.models import Genre

class User(AbstractUser):
    is_adult = models.BooleanField(default=False)
    genre = models.ManyToManyField(Genre, related_name="user")
from django.db import models
from django.conf import settings

# Create your models here.

class Genre(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self): #어떻게 보여주는가
        return self.name


class Movie(models.Model):
    title = models.CharField(max_length=100)
    original_title = models.CharField(max_length=100,null=True)
    release_date = models.DateField(null=True)
    popularity = models.FloatField(null=True)
    vote_count = models.IntegerField(null=True)
    vote_average = models.FloatField(null=True)
    adult = models.BooleanField()
    overview = models.TextField(null=True)
    original_language = models.CharField(max_length=100,null=True)
    poster_path = models.CharField(max_length=500,blank=True,null=True)
    backdrop_path = models.CharField(max_length=100,blank=True,null=True)
    genres = models.ManyToManyField(Genre, related_name="movies")
    
    like = models.ManyToManyField(settings.AUTH_USER_MODEL, through='like_time', related_name='liker')

class User_Vote(models.Model):
    cnt = models.IntegerField()
    content = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)

class like_time(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie,on_delete=models.CASCADE)
    created_at=models.DateField(auto_now_add=True)
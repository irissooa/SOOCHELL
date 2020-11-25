from django.db import models
from django.conf import settings	
from django.contrib.postgres.fields import ArrayField


class Genre(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self): 
        return self.name

class Movie(models.Model):
    title = models.CharField(max_length=100)
    original_title = models.CharField(max_length=100)
    #release_date = models.DateField(max_length=50,null=True)
    popularity = models.FloatField()
    vote_count = models.IntegerField()
    vote_average = models.FloatField()
    adult = models.BooleanField()
    overview = models.TextField()
    original_language = models.CharField(max_length=100)
    poster_path = models.CharField(max_length=500,null=True)
    backdrop_path = models.CharField(max_length=100,null=True)
    movie_id = models.IntegerField()
    genre_ids = models.ManyToManyField(Genre, related_name='movies')
    video = models.BooleanField()

    like = models.ManyToManyField(settings.AUTH_USER_MODEL,related_name='liker')


class LikeMovie(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)



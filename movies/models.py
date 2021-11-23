from django.db import models

class Genre(models.Model):
    name = models.CharField(max_length=50)

class Movie(models.Model):
    title = models.CharField(max_length=100)
    release_date = models.DateField()
    popularity = models.FloatField()
    vote_count = models.IntegerField()
    vote_average = models.FloatField()
    overview = models.TextField()
    poster_path = models.CharField(max_length=200)
    genres = models.ManyToManyField(Genre, related_name='movies')

    def __str__(self):
        return self.title

class Genre_movie(models.Model):
    title = models.CharField(max_length=100)
    release_date = models.DateField()
    ost = models.CharField(max_length=100)
    running_time = models.IntegerField(default=100)
    grade = models.FloatField(default=5.00)
    overview = models.TextField()
    poster_path = models.CharField(max_length=300)
    genres = models.ManyToManyField(Genre, related_name='genre_movies')

    def __str__(self):
        return self.title
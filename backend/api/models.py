from django.db import models
import string
import random
from django.contrib.auth.models import AbstractUser
from django.db.models import JSONField
from django.contrib.auth import get_user_model # If used custom user model


UserModel = get_user_model()


class DBSongs(models.Model):
    song_name = models.CharField(max_length=500)
    artist_name = models.CharField(max_length=500)
    bpm = models.IntegerField(default=0)
    key = models.CharField(max_length=50)
    mode = models.CharField(max_length=50)
    danceability = models.IntegerField(default=0)
    valence = models.IntegerField(default=0)
    energy = models.IntegerField(default=0)
    acousticness = models.IntegerField(default=0)
    instrumentalness = models.IntegerField(default=0)
    liveness = models.IntegerField(default=0)
    speechiness = models.IntegerField(default=0)

    def __str__(self):
        return self.song_name + ' - ' + self.artist_name


class DBUserQueries(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    description = models.CharField(max_length=500)
    data = JSONField(blank=True, null=True)

    def __str__(self):
        return str(self.user.username) + ' - ' + self.description

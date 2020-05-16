from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.

class Album(models.Model):
    artist = models.CharField(max_length=250)
    album_title = models.CharField(max_length=500)
    genre = models.CharField(max_length=100)
    album_logo = models.CharField(max_length=1000)

    def get_absolute_url(self):
        return reverse('param', kwargs={'pk': self.id})

    def __str__(self):
        return self.album_title + ' - ' + self.artist

class Song(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    file_type = models.CharField(max_length=10)
    song_title = models.CharField(max_length=250)
    audiotrack = models.FileField(upload_to='media/')
    is_favorite = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse('param', kwargs={'pk': self.album.id})

    def __str__(self):
        return self.song_title

class Comment(models.Model):
    post = models.ForeignKey(Album, on_delete=models.CASCADE)
    author = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text
    
    def get_absolute_url(self):
        return reverse('param', kwargs={'pk': self.post.id})


class Review(models.Model):
    review_title = models.CharField(max_length=100)
    review_artist = models.CharField(max_length=100)
    review_author = models.CharField(max_length=200, default="")
    review_logo = models.CharField(max_length=1000)
    review_text = models.TextField()
    review_grade = models.IntegerField(
        default=1,
        validators=[MaxValueValidator(10), MinValueValidator(1)]
     )
    def get_absolute_url(self):
        return reverse('revparam', kwargs={'pk': self.id})

    def __str__(self):
        return self.review_title

class ReviewComment(models.Model):
    post = models.ForeignKey(Review, on_delete=models.CASCADE)
    author = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text
    
    def get_absolute_url(self):
        return reverse('revparam', kwargs={'pk': self.post.id})
from django.contrib import admin
from .models import Album, Song, Comment, Review, ReviewComment
# Register your models here.

admin.site.register(Album)
admin.site.register(Song)
admin.site.register(Comment)
admin.site.register(Review)
admin.site.register(ReviewComment)

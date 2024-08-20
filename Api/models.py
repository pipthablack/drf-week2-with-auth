from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings  # Import settings to get the custom user model

# Create your models here.

class WatchList(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    platform = models.ForeignKey('StreamPlatform', on_delete=models.CASCADE, related_name="watchlist")
    active = models.BooleanField(default=True)
    avg_rating = models.FloatField(default=0)
    number_rating = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    

class StreamPlatform(models.Model):
    name = models.CharField(max_length=30)
    about = models.CharField(max_length=150)
    website = models.URLField(max_length=100)

    def __str__(self):
        return self.name
    
class Review(models.Model):
    review_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) 
    rating = models.IntegerField(default=0, validators=[MinValueValidator(1), MaxValueValidator(5)])
    watchlist = models.ForeignKey('Watchlist', on_delete=models.CASCADE, related_name='reviews')
    description = models.CharField(max_length=200)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now_add=True)
       
    
    def __str__(self):
        return str(self.rating) + " | " + self.watchlist.title + " | " + str(self.review_user)

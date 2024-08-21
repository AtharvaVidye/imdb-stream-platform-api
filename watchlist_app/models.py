from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User

class StreamPlatform(models.Model):
    name = models.CharField(max_length=50)
    about = models.CharField(max_length=150)
    website = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class Watchlist(models.Model):
    title = models.CharField(max_length=100)
    storyline = models.CharField(max_length=100)
    platform = models.ForeignKey(StreamPlatform, on_delete=models.CASCADE, related_name="watchlist")
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    avg_rating = models.FloatField(default= 0)
    number_rating = models.IntegerField(default= 0)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
    
    
    
class Review(models.Model):
    review_user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    description = models.CharField(max_length=200, null=True)
    watchlist = models.ForeignKey(Watchlist, on_delete=models.CASCADE, related_name="reviews")  # changed to lowercase 'w'
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now=True)
    update = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.rating} stars review for {self.watchlist.title}"  # changed to lowercase 'w'

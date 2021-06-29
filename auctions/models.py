from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime

CATEGORIES = (
    ("1","Electronics"),
    ("2","Outdoors"),
    ("3","Handmade"),
    ("4","Sports"),
    ("5","Baby/Kids"),
    ("6","Tools"),
)

class User(AbstractUser):
    pass

class Auction(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=200)
    startingPrice = models.FloatField()
    lastBid = models.FloatField(null=True)
    closePrice = models.FloatField(null=True)
    image = models.URLField(default="https://static.umotive.com/img/product_image_thumbnail_placeholder.png")
    duration = models.BooleanField(default=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(default=datetime.now())
    updated = models.DateTimeField(default=datetime.now())
    category = models.CharField(max_length=1, choices=CATEGORIES, default="6")
    winner = models.IntegerField(default=0, null=True)

    def __str__(self):
        return f"{self.title}"


class Bid(models.Model):
    auction = models.ForeignKey(Auction, related_name="bids", on_delete=models.CASCADE)
    amount = models.FloatField()
    win = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(default=datetime.now())

class Comment(models.Model):
    auction = models.ForeignKey(Auction, related_name="comments", on_delete=models.CASCADE)
    comment = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(default=datetime.now())

class WatchList(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="watchlist", on_delete=models.CASCADE)
    created = models.DateTimeField(default=datetime.now())




from django.db import models
from django.contrib.auth.models import AbstractUser
from articles.models import Article
from reviews.models import Review

# Create your models here.


class User(AbstractUser):
    followings = models.ManyToManyField(
        "self", symmetrical=False, related_name="follower"
    )
    marker = models.ManyToManyField(Article, related_name="articles")
    like_reviews = models.ManyToManyField(Review, related_name="like_it")

from django.db import models
from django.contrib.auth.models import AbstractUser
from articles.models import Article

# Create your models here.

class User(AbstractUser):
    followings = models.ManyToManyField(
        "self", symmetrical=False, related_name="follower"
    )
    # bookmark_users = models.ManyToManyField(AUTH_USER_MODEL, related_name="articles")

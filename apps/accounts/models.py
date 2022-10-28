from django.db import models
from config.settings import AUTH_USER_MODEL
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    @property
    def full_name(self):
        return f"{self.last_name}{self.first_name}"

    followings = models.ManyToManyField("self", symmetrical=False, related_name="followers")

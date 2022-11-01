from django.db import models
from articles.models import Article
from Camp23.settings import AUTH_USER_MODEL

# Create your models here.
class Review(models.Model):
    content = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
from django.db import models
from articles.models import Article
from Camp23.settings import AUTH_USER_MODEL
from django.core.validators import MinValueValidator, MaxValueValidator


grade_ = {}

# Create your models here.
class Review(models.Model):
    title = models.CharField(max_length=30)
    content = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    grade = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(10)]
    )

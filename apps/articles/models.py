from distutils.command.upload import upload
from django.db import models
from config.settings import AUTH_USER_MODEL
from imagekit.processors import ResizeToFill, Thumbnail
from imagekit.models import ProcessedImageField
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings

# Create your models here.
class Article(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    movie_name = models.CharField(max_length=30)
    grade = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    
    view = models.PositiveIntegerField(default=0)
    # image = ProcessedImageField(
    #     upload_to='images/', 
    #     blank=True, 
    #     processors=[ResizeToFill(1200, 960)],
    #     format="JPEG", 
    #     options={
    #         "quality": 80,
    #     },
    #     null=True)
    # thumbnail = ProcessedImageField(
    #     upload_to="thumbnail/",
    #     blank=True,
    #     processors=[Thumbnail(1200, 960)],
    #     format="JPEG",
    #     options={
    #         "quality": 60,
    #     }),
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    # like_users = models.ManyToManyField(AUTH_USER_MODEL, related_name="articles")

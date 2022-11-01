from django.db import models
from Camp23.settings import AUTH_USER_MODEL
from imagekit.processors import ResizeToFill
from imagekit.models import ProcessedImageField
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class Article(models.Model):
    thumbnail = ProcessedImageField(
        upload_to="thumbnail/",
        blank=True,
        processors=[ResizeToFill(1200, 960)],
        format="JPEG",
        options={
            "quality": 60,
        },
    )
    address = models.CharField(max_length=100)
    contact = models.CharField(max_length=14)
    geography = models.BooleanField()
    camp_type = models.CharField(max_length=20)
    season = models.CharField(max_length=20)
    active_day = models.CharField(max_length=10)
    reservation = models.CharField(max_length=15)
    amenities = models.CharField(max_length=50)
    grade = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    tags = models.BooleanField(null=True)
    # like_users = models.ManyToManyField(AUTH_USER_MODEL, related_name="articles")
    # bookmark_users = models.ManyToManyField(AUTH_USER_MODEL, related_name="articles")
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)


class Image(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    image = models.ImageField(
        default="images/default_image.jpeg",
        upload_to="images/",
        blank=True,
    )

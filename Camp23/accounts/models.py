from django.db import models
from reviews.models import Review
from articles.models import Article
from imagekit.processors import ResizeToFill
from imagekit.models import ProcessedImageField
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator, MaxLengthValidator

# Create your models here.


def input_only_number(value):
    if not value.isdigit():
        raise ValidationError("숫자만 적을 수 있습니다.")


class User(AbstractUser):
    kakao_id = models.BigIntegerField(null=True, unique=True)
    naver_id = models.CharField(null=True, unique=True, max_length=100)
    googld_id = models.CharField(null=True, unique=True, max_length=50)
    followings = models.ManyToManyField(
        "self", symmetrical=False, related_name="follower"
    )
    marker = models.ManyToManyField(Article, related_name="link_article")
    like_reviews = models.ManyToManyField(Review, related_name="reviews_like")
    like_articles = models.ManyToManyField(Article, related_name="articles_like")
    phone = models.CharField(
        max_length=13,
        validators=[MinLengthValidator(11), MaxLengthValidator(11), input_only_number],
    )
    profile_picture = ProcessedImageField(
        upload_to="profile_picture/",
        blank=True,
        processors=[ResizeToFill(64, 64)],
        format="JPEG",
        options={
            "quality": 30,
        },
    )
    social_profile_picture = models.CharField(null=True, max_length=150)

    @property
    def full_name(self):
        return f"{self.last_name}{self.first_name}"

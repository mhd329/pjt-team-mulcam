from django.db import models
from config.settings import AUTH_USER_MODEL
from imagekit.processors import ResizeToFill
from imagekit.models import ProcessedImageField
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class Article(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    ####################################################

    # 영화 이름
    # movie_name = models.CharField(max_length=30)

    # 평점
    # grade = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])

    # 작성자
    # user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)

    # 조회수
    # view = models.PositiveIntegerField(default=0)

    # 사진
    # thumbnail = ProcessedImageField(
    #     upload_to="thumbnail/",
    #     blank=True,
    #     processors=[ResizeToFill(1200, 960)],
    #     format="JPEG",
    #     options={
    #         "quality": 60,
    #     },
    # )
    # image = models.ImageField(
    #     upload_to="images/",
    #     blank=True,
    # )

    # 좋아요
    # like_users = models.ManyToManyField(AUTH_USER_MODEL, related_name="articles")

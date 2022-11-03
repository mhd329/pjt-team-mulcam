from django.db import models
from articles.models import Article
from Camp23.settings import AUTH_USER_MODEL
from django.core.validators import MinValueValidator, MaxValueValidator
from multiselectfield import MultiSelectField

tag = [
    (1, "별 보기 좋은"),
    (2, "시원한 여름"),
    (3, "파티가 있는"),
    (4, "가족이랑"),
    (5, "커플"),
    (6, "조용한"),
    (7, "애견동반"),
    (8, "도심 속 캠핑장"),
    (9, "풍경이 좋은"),
    (10, "2030인기"),
    (11, "바다가 보이는"),
]


grade_ = []

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
    tag = MultiSelectField(choices=tag, max_choices=3)

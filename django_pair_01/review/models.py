from django.db import models

# Create your models here.
class Review(models.Model):
    # 리뷰 제목
    # 리뷰 내용
    # 리뷰 생성시간
    # 최근 리뷰 업데이트
    title = models.CharField(max_length=80)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

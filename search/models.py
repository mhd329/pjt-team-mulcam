from django.db import models

# Create your models here.


class Search(models.Model):
    keyword = models.CharField(max_length=30)
    count = models.IntegerField(default=0)

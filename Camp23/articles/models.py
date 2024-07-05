from django.db import models
from Camp23.settings import AUTH_USER_MODEL
from imagekit.processors import ResizeToFill
from multiselectfield import MultiSelectField
from imagekit.models import ProcessedImageField

amenities_list = (
    (1, "화장실"),
    (2, "전기"),
    (3, "개수대"),
    (4, "샤워실"),
    (5, "온수"),
    (6, "와이파이"),
    (7, "펫"),
)
local_map = (
    (1, "경기도"),
    (2, "강원도"),
    (3, "충청도"),
    (4, "경상도"),
    (5, "전라도"),
    (6, "제주도"),
)

# Create your models here.
class Article(models.Model):
    name = models.CharField(max_length=30)
    image = models.ImageField(
        default="images/default_image.jpeg",
        upload_to="images/",
        blank=True,
    )
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
    contact = models.CharField(max_length=40)
    camp_type = models.CharField(max_length=20)
    season = models.CharField(max_length=20)
    active_day = models.CharField(max_length=20)
    homepage = models.CharField(max_length=200, blank=True)
    reservation = models.CharField(max_length=15)
    amenities = MultiSelectField(choices=amenities_list)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    geography = models.CharField(max_length=20)
    local = models.IntegerField(choices=local_map)


class Photo(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(
        default="photos/default_image.jpeg",
        upload_to="photos/",
        blank=True,
    )

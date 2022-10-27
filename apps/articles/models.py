from django.db import models
from config.settings import AUTH_USER_MODEL
from imagekit.processors import ResizeToFill
from imagekit.models import ProcessedImageField
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

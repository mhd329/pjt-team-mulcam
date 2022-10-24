from django.db import models
from config.settings import AUTH_USER_MODEL
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator, MaxLengthValidator


def input_only_number(value):
    if not value.isdigit():
        raise ValidationError("숫자만 적을 수 있습니다.")


# Create your models here.
class User(AbstractUser):
    followers = models.ManyToManyField(AUTH_USER_MODEL, related_name="followings")

    @property
    def full_name(self):
        return f"{self.last_name}{self.first_name}"


class UserPhoneNumber(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(
        max_length=13,
        validators=[MinLengthValidator(11), MaxLengthValidator(11), input_only_number],
        blank=True,
    )

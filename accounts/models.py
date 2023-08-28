import os
import time
import hmac
import base64
import hashlib
import requests
from django.db import models
from dotenv import load_dotenv
from imagekit.processors import ResizeToFill
from imagekit.models import ProcessedImageField
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import MinLengthValidator, MaxLengthValidator


def input_only_number(value):
    if not value.isdigit():
        raise ValidationError("숫자만 적을 수 있습니다.")


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:  # 추상 클래스로 정의함
        abstract = True


class User(AbstractUser):
    # 필수 항목 필드
    username = models.CharField(
        error_messages={"unique": "같은 아이디가 이미 존재합니다."},
        unique=True,
        max_length=16,
        validators=[UnicodeUsernameValidator()],
        verbose_name="아이디",
    )
    # 선택 항목 필드
    fullname = models.CharField(
        max_length=20,
        null=True,
        blank=True,
    )
    nickname = models.CharField(
        max_length=20,
        null=True,
        blank=True,
    )
    email = models.EmailField(
        null=True,
        blank=True,
        max_length=254,
        verbose_name="이메일 주소",
    )
    phone = models.CharField(
        max_length=13,
        validators=[MinLengthValidator(11), MaxLengthValidator(11), input_only_number],
        null=True,
        blank=True,
    )
    profile_picture = ProcessedImageField(
        upload_to="profile_pictures/",
        null=True,
        blank=True,
        processors=[ResizeToFill(512, 512)],
        format="JPEG",
        options={
            "quality": 80,
        },
    )
    address = models.CharField(max_length=100)
    detail_address = models.CharField(max_length=30)
    # 소셜 아이디 관련 필드
    is_social_account = models.BooleanField(default=False)
    git_username = models.CharField(null=True, blank=True, max_length=50)
    boj_username = models.CharField(null=True, blank=True, max_length=50)
    service_name = models.CharField(null=True, max_length=20)
    social_id = models.CharField(null=True, blank=True, max_length=100)
    social_profile_picture = models.CharField(null=True, blank=True, max_length=150)
    # 인증 필드
    is_phone_active = models.BooleanField(default=False)
    is_email_active = models.BooleanField(default=False)
    token = models.CharField(max_length=150, null=True, blank=True)
    followings = models.ManyToManyField(
        "self", symmetrical=False, related_name="followers"
    )

    @property
    def full_name(self):
        return f"{self.last_name}{self.first_name}"

    def __str__(self):
        return self.username


load_dotenv()


class AuthPhone(TimeStampedModel):
    phone = models.IntegerField()
    auth_count = models.IntegerField()

    NAVER_CLOUD_ACCESS_KEY = os.getenv("NAVER_CLOUD_ACCESS_KEY")
    NAVER_CLOUD_SECRET_KEY = os.getenv("NAVER_CLOUD_SECRET_KEY")
    NAVER_CLOUD_SERVICE_ID = os.getenv("NAVER_CLOUD_SERVICE_ID")

    def save(self, *args, **kwargs):  # save 메서드 재정의
        # 문자 보내기 단계에서 AuthPhone 인스턴스를 새로 만드는데, 그 과정에서 랜덤한 인증번호가 생성된다.
        # 그래서 그 번호를 auth_number에 저장하고,
        super().save(*args, **kwargs)  # 그 외 다른 변경사항들을 반영하기 위해 세이브 하면,
        self.send_sms()  # 문자가 전송되게끔 바꾼것이다.
        # 즉, 인증번호가 생성되고 유효기간이 카운팅됨과 동시에 문자가 전송되는 구조이다.

    def send_sms(self):
        timestamp = str(int(time.time() * 1000))
        access_key = self.NAVER_CLOUD_ACCESS_KEY
        secret_key = bytes(self.NAVER_CLOUD_SECRET_KEY, "UTF-8")
        service_id = self.NAVER_CLOUD_SERVICE_ID
        method = "POST"
        uri = f"/sms/v2/services/{service_id}/messages"
        message = method + " " + uri + "\n" + timestamp + "\n" + access_key
        message = bytes(message, "UTF-8")  # ascii문자 외의 문자 전송을 보장하기위해 bytes로 변환
        signing_key = base64.b64encode(
            hmac.new(secret_key, message, digestmod=hashlib.sha256).digest()
        )
        url = f"https://sens.apigw.ntruss.com/sms/v2/services/{service_id}/messages"
        # 선택사항은 제외하고 필수사항만 설정
        headers = {
            "Content-Type": "application/json; charset=utf-8",
            "x-ncp-apigw-timestamp": timestamp,  # 에포크시간
            "x-ncp-iam-access-key": access_key,  # 발급받은 access key
            "x-ncp-apigw-signature-v2": signing_key,  # 가이드에서 권장방식대로 사이닝키 만들어서 제출
        }
        data = {
            "type": "SMS",
            "from": "01099453849",
            "content": f"[코드비] 인증 번호 [{self.auth_number}]를 입력해주세요.",
            "messages": [{"to": f"{self.phone}"}],
        }
        # 여기서 인증번호가 보내짐
        requests.post(url, headers=headers, json=data)

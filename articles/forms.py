from django import forms
from .models import Article, Photo


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = (
            "name",
            "image",
            "thumbnail",
            "address",
            "contact",
            "homepage",
            "camp_type",
            "season",
            "active_day",
            "reservation",
            "geography",
            "amenities",
            "local",
        )

        labels = {
            "name": "캠핑장명",
            "image": "메인이미지",
            "thumbnail": "썸네일이미지",
            "address": "주소",
            "contact": "연락처",
            "homepage": "홈페이지",
            "camp_type": "테마(환경)",
            "season": "이용시간",
            "active_day": "이용요금",
            "reservation": "예약방법",
            "geography": "바닥유형",
            "amenities": "편의시설",
            "local": "지역",
        }


class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ("image",)

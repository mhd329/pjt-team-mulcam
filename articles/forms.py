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
            "camp_type",
            "season",
            "active_day",
            "reservation",
            "geography",
            "amenities",
        )


class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ("image",)

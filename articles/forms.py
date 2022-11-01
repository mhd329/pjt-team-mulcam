from django import forms
from .models import Article, Image


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = (
            "thumbnail",
            "address",
            "contact",
            "geography",
            "camp_type",
            "season",
            "active_day",
            "reservation",
            "amenities",
            "tags",
        )


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ("image",)

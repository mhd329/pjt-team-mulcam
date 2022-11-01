from django import forms
from .models import Article, SubImage


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = (
            "image",
            "thumbnail",
            "address",
            "contact",
            "camp_type",
            "season",
            "active_day",
            "reservation",
            "amenities",
        )


class SubImageForm(forms.ModelForm):
    class Meta:
        model = SubImage
        fields = ("sub_image",)

from dataclasses import fields
from django import forms

from apps.articles.models import Article


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = (
            "title",
            "content",
            "created_at",
            "updated_at",
        )

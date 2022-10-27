from dataclasses import fields
from django import forms

from apps.articles.models import Article


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = (
            "title",
            "content",
            "movie_name",
            "grade",
            # "created_at",
            # "updated_at",
            # "image",
            # "thumbnail"
        )

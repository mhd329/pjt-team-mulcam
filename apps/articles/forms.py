from django import forms

from apps.articles.models import Article, Comment


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = (
            "title",
            "content",
            "movie_name",
            "grade",
            # "image",
            # "thumbnail"
        )

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content',]
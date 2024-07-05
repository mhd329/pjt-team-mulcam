from django import forms
from .models import Review


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["title", "movie_name", "content", "grade"]
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "placeholder": "제목은 80자 이내로 작성해주세요.",
                    "style": "height: 2.5rem; resize: none;",
                }
            ),
            "content": forms.Textarea(
                attrs={
                    "placeholder": "",
                    "style": "height: 15rem; resize: none;",
                }
            ),
            "movie_name": forms.Textarea(
                attrs={
                    "placeholder": "",
                    "style": "height: 2.5rem; resize: none;",
                }
            ),
        }
        labels = {
            "title": "제목",
            "content": "내용",
            "movie_name": "영화 제목",
            "grade": "평점",
        }

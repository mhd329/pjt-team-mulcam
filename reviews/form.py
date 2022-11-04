from django import forms
from .models import Review
from .widgets import starWidget


class CreateReview(forms.ModelForm):
    class Meta:
        model = Review
        fields = [
            "title",
            "content",
            "tag",
            "grade",
        ]
        widgets = {"grade": starWidget}
        labels = {"title": "제목", "content": "본문", "grade": "평점", "tag": "Tag"}

from django import forms
from .models import UserPhoneNumber
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class CreateUserForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ["username"]


class ChangeUserInfo(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = [
            "last_name",
            "first_name",
            "email",
        ]


class UserPhoneNumberForm(forms.ModelForm):
    class Meta:
        model = UserPhoneNumber
        fields = ("phone",)
        labels = {
            "phone": "휴대폰",
        }
        widgets = {
            "phone": forms.TextInput(
                attrs={
                    "placeholder": "'-' 를 제외하고 입력해주세요.",
                    "style": "width: 100%; resize: none;",
                }
            ),
        }

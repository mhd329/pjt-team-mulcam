from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (
    UserCreationForm,
    UserChangeForm,
    PasswordChangeForm,
)


class CreateUserForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ("username",)
        exclude = ("phone",)
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


class ChangeUserInfo(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = (
            "first_name",
            "last_name",
            "email",
            "phone",
        )
        widgets = {
            "last_name": forms.TextInput(
                attrs={
                    "placeholder": "",
                }
            ),
            "first_name": forms.TextInput(
                attrs={
                    "placeholder": "",
                }
            ),
            "email": forms.TextInput(
                attrs={
                    "placeholder": "",
                }
            ),
            "phone": forms.TextInput(
                attrs={
                    "placeholder": "'-' 를 제외하고 입력해주세요.",
                    "style": "width: 100%; resize: none;",
                }
            ),
        }


class ChangePasswordForm(PasswordChangeForm):
    pass

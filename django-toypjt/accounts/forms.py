from django import forms
from .models import UserPhoneNumber
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (
    UserCreationForm,
    UserChangeForm,
    PasswordChangeForm,
)


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = (
            "username",
            "last_name",
            "first_name",
            "email",
        )
        widgets = {
            "username": forms.TextInput(
                attrs={
                    "placeholder": "",
                }
            ),
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
        }


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = (
            "username",
            "last_name",
            "first_name",
            "email",
        )
        widgets = {
            "username": forms.TextInput(
                attrs={
                    "placeholder": "",
                }
            ),
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
        }


class CustomPasswordChangeForm(PasswordChangeForm):
    def clean_new_password1(self):
        old = self.cleaned_data.get("old_password")
        new = self.cleaned_data.get("new_password1")
        if old == new:
            raise forms.ValidationError("이전 비밀번호와 새 비밀번호가 같습니다.")


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

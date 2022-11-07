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
    def clean_new_password1(self):
        old_password = self.cleaned_data.get("old_password")
        new_password1 = self.cleaned_data.get("new_password1")
        if old_password == new_password1:
            raise forms.ValidationError("이전 비밀번호와 새 비밀번호가 같습니다.")
        return new_password1

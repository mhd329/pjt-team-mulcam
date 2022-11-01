from dataclasses import field
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django.contrib.auth import get_user_model




class CreateUserForm(UserCreationForm):
    class Meta:
        model=get_user_model()
        fields=["username"]

class ChangeUserInfo(UserChangeForm):
    class Meta:
        model=get_user_model()
        fields= ["email"]
from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path("", views.user_list, name="user-list"),
    path("signup/", views.signup, name="signup"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("<int:pk>/profile/", views.profile, name="profile"),
    path("update/", views.update, name="update"),
    path("<int:pk>/follow/", views.follow, name="follow"),
    path("password/", views.change_password, name="change_password"),
]

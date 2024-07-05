from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path("", views.index, name="index"),
    path("signup/", views.signup, name="signup"),
    path("login/", views.login, name="login"),
    path("<int:pk>/", views.detail, name="detail"),
    path("<int:pk>/update/", views.update, name="update"),
    path("password/", views.change_pw, name="change-pw"),
    path("logout/", views.logout, name="logout"),
    path("delete/", views.delete, name="delete"),
]

from django.urls import path
from . import views

app_name = "index"

urlpatterns = [
    path("", views.index, name="index"),
    path("intro/", views.intro, name="intro"),
    path("contrib/", views.contrib, name="contrib"),
]
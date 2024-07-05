from django.urls import path
from . import views

app_name = "main"

urlpatterns = [
    path("index", views.index, name="index"),
    path("all/", views.all, name="all"),
    path("<int:pk>/theme/", views.theme, name="theme"),
    path("", views.first, name="first"),
]

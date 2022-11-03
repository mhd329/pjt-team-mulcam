from django.urls import path
from . import views

app_name = "main"

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:pk>/theme/", views.theme, name="theme"),
]

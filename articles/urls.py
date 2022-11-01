from django.urls import path
from . import views

app_name = "articles"

urlpatterns = [
    path("", views.camp01, name="camp01"),
]

from django.urls import path
from . import views

app_name = "articles"

urlpatterns = [
    path("camp01/", views.camp01, "reviews/camp01.html"),
]

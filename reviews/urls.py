from django.urls import path
from . import views

app_name = "reviews"

urlpatterns = [
    path("list/", views.list, "reviews/list.html"),
]

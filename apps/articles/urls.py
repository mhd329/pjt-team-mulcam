from django.urls import path
from . import views

app_name = "articles"

urlpatterns = [
    path("reviews/", views.reviews, name="reviews")
]

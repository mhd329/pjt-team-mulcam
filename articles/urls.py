from django.urls import path
from . import views

app_name = "articles"

urlpatterns = [
    path("<int:pk>/", views.detail, name="detail"),
    path("<int:pk>/photos/", views.photos, name="photos"),
    path("<int:pk>/add-image/", views.add_image, name="add-image"),
]

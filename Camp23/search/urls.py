from django.urls import path
from . import views

app_name = "search"

urlpatterns = [
    path("search/", views.search, name="search"),
    path("<int:pk>/k_map/", views.k_map, name="k_map"),
]

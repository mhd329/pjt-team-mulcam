from django.urls import path
from . import views

app_name = "reviews"

urlpatterns = [
    path("<int:article_pk>/create/", views.create, name="create"),
    path("review_list/", views.review_list, name="review_list"),
    path("<int:review_pk>/detail/", views.detail, name="detail"),
    path("<int:review_pk>/update/", views.update, name="update"),
]

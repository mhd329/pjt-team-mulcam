from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path("signup/", views.signup, name="signup"),
    path("login/", views.login, name="login"),
    path("<int:user_pk>/detail/", views.detail, name="detail"),
    path("<int:user_pk>/update/", views.update, name="update"),
    path("logout/", views.logout, name="logout"),
    path("<int:user_pk>/follow/", views.follow, name="follow"),
    path("<int:user_pk>/delete/", views.delete, name="delete"),
    path("<int:user_pk>/password/", views.change_pw, name="password"),
    path("<int:article_pk>/marker/", views.marker, name="marker"),
    path("<int:review_pk>/like_reviews/", views.like_reviews, name="like_reviews"),
    path("<int:article_pk>/like_articles/", views.like_articles, name="like_articles"),
    path("login/kakao/", views.kakao_request, name="kakao"),
    path("login/kakao/callback/", views.kakao_callback),
    path("login/naver/", views.naver_request, name="naver"),
    path("login/naver/callback/", views.naver_callback),
]

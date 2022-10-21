from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = "articles"


urlpatterns = [
    path("", views.index, name="index"),
    path("create/", views.create, name="create"),
    path("<int:pk>/", views.detail, name="detail"),
    path("<int:pk>/delete/", views.delete, name="delete"),
    path("update/<int:pk>", views.update, name='update'),
    path('<int:pk>/comments/<int:comment_pk>', views.comment_delete, name='comment_delete'),
    path('intro/', views.intro, name="intro"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
from .models import Article, Photo
from articles.forms import PhotoForm
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from reviews.models import Review

# Create your views here.


def detail(request, pk):
    article = Article.objects.get(id=pk)
    reviews = Review.objects.filter(article_id=article.pk)
    context = {
        "reviews": reviews,
        "article": article,
        "photos": article.photo_set.order_by("-id")[:3],
    }
    return render(request, "articles/detail.html", context)


def photos(request, pk):
    article = Article.objects.get(pk=pk)
    photos = article.photo_set.all()
    context = {
        "photos": photos,
    }
    return render(request, "articles/photos.html", context)


def add_photo(request, pk):
    article = Article.objects.get(pk=pk)
    if request.method == "POST":
        photo_form = PhotoForm(request.POST, request.FILES)
        if photo_form.is_valid():
            photo = photo_form.save(commit=False)
            photo.article = article
            photo.user = request.user
            photo.save()
            return redirect("articles:detail", article.pk)
    else:
        photo_form = PhotoForm()
    context = {
        "photo_form": photo_form,
    }
    return render(request, "articles/photo-form.html", context)


def delete(request, article_pk):
    article = Article.objects.get(pk=article_pk)
    if request.user.is_superuser:
        article.delete()
    redirect("main:index")


def information(request):
    return render(request, "articles/information.html")

from .models import Article, Image
from articles.forms import ImageForm
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model

# Create your views here.
def detail(request, pk):
    article = Article.objects.get(id=pk)
    context = {
        "article": article,
        "images": article.image_set.all,
    }
    return render(request, "articles/detail.html", context)


def photos(request, pk):
    article = Article.objects.get(pk=pk)
    images = article.image_set.order_by("-id")
    context = {
        "images": images,
    }
    return render(request, "articles/photos.html", context)


def add_image(request, pk):
    article = Article.objects.get(pk=pk)
    if request.method == "POST":
        image_form = ImageForm(request.POST, request.FILES)
        if image_form.is_valid():
            image = image_form.save(commit=False)
            image.article = article
            image.user = request.user
            image.save()
            return redirect("articles:detail", article.pk)
    else:
        image_form = ImageForm()
    context = {
        "image_form": image_form,
    }
    return render(request, "articles/detail.html", context)

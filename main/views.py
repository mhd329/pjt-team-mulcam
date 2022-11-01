from multiprocessing import context
from django.shortcuts import render
from articles.models import Article

# Create your views here.


def index(request):
    all_article = Article.objects.all()

    context = {"all_article": all_article}

    return render(request, "main/index.html", context)

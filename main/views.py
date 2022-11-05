from django.shortcuts import render
from articles.models import Article
from search.models import Search

# Create your views here.


def index(request):
    all_article = Article.objects.all()

    carousel_articles = Article.objects.order_by("-pk")[:3]
    hot_keyword = Search.objects.all().order_by("-count")[:5]
    context = {
        "carousel_articles": carousel_articles,
        "all_article": all_article,
        "hot_keyword": hot_keyword,
    }
    return render(request, "main/index.html", context)


def theme(request, pk):
    if pk == 1:
        theme = "산"
    elif pk == 2:
        theme = "강"
    elif pk == 3:
        theme = "바다"
    elif pk == 4:
        theme = "도심"
    filter_article = Article.objects.filter(camp_type__contains=theme)

    context = {
        "filter_article": filter_article,
        "theme": theme,
    }

    return render(request, "main/theme.html", context)


def all(request):
    all_article = Article.objects.all()

    context = {
        "all_article": all_article,
    }

    return render(request, "main/all.html", context)

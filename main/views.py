from django.shortcuts import render
from articles.models import Article
from search.models import Search

# Create your views here.


def index(request):
    all_article = Article.objects.all()
    hot_keyword = Search.objects.all().order_by()[:5]

    context = {
        "all_article": all_article,
        "hot_keyword": hot_keyword,
    }

    return render(request, "main/index.html", context)

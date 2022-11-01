from django.shortcuts import render
from .models import Article

# Create your views here.
def detail(request, pk):
    article = Article.objects.get(id=pk)
    context = {
        "article": article,
        "images" : article.image_set.all,
    }
    return render(request, "articles/detail.html", context)

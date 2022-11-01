from django.shortcuts import render
from .models import Article

# Create your views here.
def detail(request, pk):
    article = Article.objects.get(id=pk)
    context = {
        "article": article,
    }
    return render(request, "articles/detail.html", context)

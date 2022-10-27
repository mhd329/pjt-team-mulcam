from django.shortcuts import render, redirect

from apps.articles.models import Article

# Create your views here.
def reviews(request):
    articles = Article.objects.order_by("-id")
    context = {
        "articles": articles,
    }
    return render(request, "articles/reviews.html", context)

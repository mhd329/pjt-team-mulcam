from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from apps.articles.models import Article
from .forms import ArticleForm

# Create your views here.
def reviews(request):
    articles = Article.objects.order_by("-id")
    context = {
        "articles": articles,
    }
    return render(request, "articles/reviews.html", context)

@login_required
def create(request):
    if request.method == 'POST':
        article_form = ArticleForm(request.POST, request.FILES)
        if article_form.is_valid():
            article = article_form.save(commit=False)
            article.user = request.user
            article.save()
            return redirect("articles:reviews")
        
    else:
        article_form = ArticleForm()
        
    context = {
        'article_form': article_form
    }
    return render(request, "articles/forms.html", context=context)
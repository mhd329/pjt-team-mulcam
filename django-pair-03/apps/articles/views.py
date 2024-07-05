from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from apps.articles.models import Article, Comment
from .forms import ArticleForm, CommentForm
from django.db.models import Q
from django.contrib.auth import get_user_model

# Create your views here.
def reviews(request):
    articles = Article.objects.order_by("-id")
    context = {
        "articles": articles,
    }
    return render(request, "articles/reviews.html", context)


@login_required
def create(request):
    if request.method == "POST":
        article_form = ArticleForm(request.POST, request.FILES)
        if article_form.is_valid():
            article = article_form.save(commit=False)
            article.user = request.user
            article.save()
            return redirect("articles:reviews")

    else:
        article_form = ArticleForm()

    context = {"article_form": article_form}
    return render(request, "articles/forms.html", context=context)


def detail(request, pk):
    article = Article.objects.get(pk=pk)
    comment_form = CommentForm()
    context = {
        "comment_form": comment_form,
        "article": article,
    }
    return render(request, "articles/detail.html", context)


def update(request, pk):
    article = Article.objects.get(pk=pk)
    if request.user == article.user:
        if request.method == "POST":
            article_form = ArticleForm(request.POST, request.FILES, instance=article)
            if article_form.is_valid():
                article_form.save()
                return redirect("articles:detail", article.pk)
        else:
            article_form = ArticleForm(instance=article)
        context = {"article_form": article_form}
        return render(request, "articles/forms.html", context)
    else:
        return redirect("articles:detail", article.pk)


@login_required
def like(request, pk):
    user = request.user
    article = Article.objects.get(id=pk)
    if article.like_users.filter(id=user.id).exists():
        article.like_users.remove(user)
        return redirect("articles:detail", article.pk)
    else:
        article.like_users.add(user)
        return redirect("articles:detail", article.pk)


def delete(request, pk):
    Article.objects.get(pk=pk).delete()
    return redirect("articles:reviews")


@login_required
def comment_create(request, pk):
    article = Article.objects.get(pk=pk)
    comment_form = CommentForm(request.POST)

    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.article = article
        comment.user = request.user
        comment.save()

    return redirect("articles:detail", article.pk)


def comment_delete(request, article_pk, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)
    comment.delete()

    return redirect("articles:detail", article_pk)


def search(request):
    if request.method == "POST":
        search = request.POST["search"]
        searched_users = get_user_model().objects.filter(username__contains=search)
        searched_articles = Article.objects.filter(
            Q(title__icontains=search)
            | Q(content__icontains=search)
            | Q(movie_name__icontains=search)
        )
        context = {
            "search": search,
            "searched_users": searched_users,
            "searched_articles": searched_articles,
        }
        return render(request, "articles/reviews.html", context)

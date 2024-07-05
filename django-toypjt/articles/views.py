from .forms import ArticleForm, CommentForm, MiniCommentForm
from django.contrib.auth.decorators import login_required
from datetime import date, datetime, timedelta
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from .models import Article, Comment
from django.contrib import messages
from django.db.models import Q

# Create your views here.
def reviews(request):
    articles = Article.objects.order_by("-id")
    context = {
        "articles": articles,
    }
    return render(request, "articles/reviews.html", context)


@login_required
def create(request):
    user = request.user
    if request.method == "POST":
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.user = user
            article.save()
            messages.success(request, "작성하였습니다.")
            return redirect("articles:reviews")
    else:
        form = ArticleForm()
    context = {
        "form": form,
    }
    return render(request, "articles/form.html", context)


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


def detail(request, pk):
    target_article = Article.objects.get(id=pk)
    likes = target_article.like_users.all()
    like_count = likes.count()
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.article = target_article
            comment.user = request.user
            comment.save()
            messages.success(request, "작성하였습니다.")
            return redirect("articles:detail", target_article.pk)
    else:
        form = CommentForm()
    context = {
        "like_count": like_count,
        "article": target_article,
        "likes": likes,
        "form": form,
    }
    response = render(request, "articles/detail.html", context)
    # 조회수 로직 긁어옴
    # 올바른 작동에 대한 보장이 없기 때문에 일단 보류해두었음
    # expire_date, now = datetime.now(), datetime.now()
    # expire_date += timedelta(days=1)
    # expire_date = expire_date.replace(hour=0, minute=0, second=0, microsecond=0)
    # expire_date -= now
    # max_age = expire_date.total_seconds()
    # cookie_value = request.COOKIES.get("hitboard", "_")
    # if not f"_{pk}_" in cookie_value:
    #     cookie_value += f"{pk}_"
    #     response.set_cookie(
    #         "hitboard", value=cookie_value, max_age=max_age, httponly=True
    #     )
    #     target_article.view += 1
    #     target_article.save()
    target_article.view += 1
    target_article.save()
    return response


@login_required
def update(request, pk):
    user = request.user
    article = Article.objects.get(id=pk)
    likes = article.like_users.all()
    if request.method == "POST":
        form = ArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            form.save()
            messages.success(request, "수정되었습니다.")
            return redirect("articles:detail", article.pk)
    else:
        form = ArticleForm(instance=article)
    context = {
        "likes": likes,
        "form": form,
        "user": user,
        "article": article,
    }
    return render(request, "articles/form.html", context)


@login_required
def delete(request, pk):
    article = Article.objects.get(id=pk)
    user = request.user
    if request.method == "POST":
        article.delete()
        messages.success(request, "삭제되었습니다.")
        return redirect("articles:reviews")
    context = {
        "article": article,
        "user": user,
    }
    return render(request, "articles/delete.html", context)


@login_required
def comment_update(request, article_pk, comment_pk):
    form = CommentForm()
    user = request.user
    article = Article.objects.get(id=article_pk)
    likes = article.like_users.all()
    target_comment = Comment.objects.get(id=comment_pk)
    if user.pk == target_comment.user.pk:
        if request.method == "POST":
            comment_form = MiniCommentForm(request.POST, instance=target_comment)
            if comment_form.is_valid():
                comment_form.save()
                messages.success(request, "수정되었습니다.")
                return redirect("articles:detail", article.pk)
        else:
            comment_form = MiniCommentForm(instance=target_comment)
        context = {
            "target_comment": target_comment,
            "comment_form": comment_form,
            "article": article,
            "likes": likes,
            "form": form,
            "user": user,
        }
        return render(request, "articles/detail.html", context)
    else:
        messages.warning(request, "권한이 없습니다.")
        return redirect("articles:detail", article_pk)


@login_required
def comment_delete(request, article_pk, comment_pk):
    comment = Comment.objects.get(id=comment_pk)
    user = request.user
    if user.pk == comment.user.pk:
        comment.delete()
        messages.success(request, "삭제되었습니다.")
        return redirect("articles:detail", article_pk)
    else:
        messages.warning(request, "권한이 없습니다.")
        return redirect("articles:detail", article_pk)


@login_required
def add_like(request, pk):
    user = request.user
    article = Article.objects.get(id=pk)
    if article.like_users.filter(id=user.id).exists():
        article.like_users.remove(user)
        return redirect("articles:detail", article.pk)
    else:
        article.like_users.add(user)
    return redirect("articles:detail", article.pk)


# 에러 처리


def error_400(request, exception):
    return render(request, "400.html", status=400)


def error_403(request, exception):
    return render(request, "403.html", status=403)


def error_404(request, exception):
    return render(request, "404.html", status=404)


def error_500(request):
    return render(request, "500.html", status=500)

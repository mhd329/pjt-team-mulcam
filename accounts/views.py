from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .form import CreateUserForm, ChangeUserInfo, ChangePasswordForm
from django.contrib.auth import get_user_model, login as my_login, logout as my_logout
from articles.models import Article
from reviews.models import Review

# Create your views here.


def signup(request):
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            my_login(request, user)
            return redirect("main:index")
    else:
        form = CreateUserForm()
    context = {
        "form": form,
    }
    return render(request, "accounts/signup.html", context)


def login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            my_login(request, form.get_user())
            return redirect(request.GET.get("next") or "main:index")
    else:
        form = AuthenticationForm()
    context = {"form": form}
    return render(request, "accounts/login.html", context)


@login_required
def logout(request):
    my_logout(request)
    return redirect("main:index")


def detail(request, user_pk):
    pick_user = get_object_or_404(get_user_model(), pk=user_pk)

    context = {"pick_user": pick_user}
    return render(request, "accounts/detail.html", context)


@login_required
def update(request, user_pk):
    pick_user = get_object_or_404(get_user_model(), pk=user_pk)
    if request.user == pick_user:
        if request.method == "POST":
            form = ChangeUserInfo(request.POST, instance=pick_user)
            if form.is_valid():
                user = form.save(commit=False)
                phone = user.phone
                if phone:
                    p1 = "".join(phone[:3])
                    p2 = "".join(phone[3:7])
                    p3 = "".join(phone[7:])
                    phone = "-".join([p1, p2, p3])
                    user.phone = phone
                else:
                    pass
                user.save()
                return redirect("accounts:detail", user_pk)
        else:
            form = ChangeUserInfo(instance=pick_user)
        context = {
            "form": form,
            "pick_user": pick_user,
        }
    return render(request, "accounts/update.html", context)


@login_required
def follow(request, user_pk):
    pick_user = get_object_or_404(get_user_model(), pk=user_pk)
    if request.user == pick_user:
        pass
    elif pick_user.followings.filter(pk=request.user.pk).exists():
        pick_user.followings.remove(request.user)
    else:
        pick_user.followings.add(request.user)
    return redirect("accounts:detail", user_pk)


@login_required
def delete(request, user_pk):
    pick_user = get_user_model().objects.get(pk=user_pk)
    if request.user == pick_user:
        pick_user.delete()
    return redirect("main:index")


@login_required
def change_pw(request, user_pk):
    pick_user = get_user_model().objects.get(pk=user_pk)
    if request.method == "POST":
        form = ChangePasswordForm(pick_user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect("accounts:detail", user_pk)
    else:
        form = ChangePasswordForm(pick_user)
    context = {
        "form": form,
    }
    return render(request, "accounts/password.html", context)


@login_required
def marker(request, article_pk):
    pick_article = get_object_or_404(Article, pk=article_pk)
    if request.user.marker.filter(pk=pick_article.pk):
        request.user.marker.remove(pick_article)
    else:
        request.user.marker.add(pick_article)
    return redirect("articles:detail", article_pk)


@login_required
def like_reviews(request, review_pk):
    pick_reviews = get_object_or_404(Review, pk=review_pk)
    if request.user.like_reviews.filter(pk=pick_reviews.pk):
        request.user.like_reviews.remove(pick_reviews)
    else:
        request.user.like_reviews.add(pick_reviews)
    return redirect("reviews:detail", review_pk)


@login_required
def like_articles(request, article_pk):
    pick_article = get_object_or_404(Article, pk=article_pk)
    if request.user.like_articles.filter(pk=pick_article.pk):
        request.user.like_articles.remove(pick_article)
    else:
        request.user.like_articles.add(pick_article)
    return redirect("articles:detail", article_pk)

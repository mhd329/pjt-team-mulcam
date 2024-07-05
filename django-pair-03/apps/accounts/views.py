from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.contrib.auth import get_user_model, update_session_auth_hash


# Create your views here.


def user_list(request):
    users = get_user_model().objects.order_by("-id")
    context = {
        "users": users,
    }
    return render(request, "accounts/user-list.html", context)


def profile(request, pk):
    user = get_user_model().objects.get(id=pk)
    context = {
        "user": user,
    }
    return render(request, "accounts/profile.html", context)


def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect("articles:reviews")
    else:
        form = CustomUserCreationForm()
    context = {
        "form": form,
    }
    return render(request, "accounts/signup.html", context)


def login(request):
    if request.method == "POST":
        form = AuthenticationForm(request.POST, data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect("articles:reviews")
    else:
        form = AuthenticationForm()
    context = {
        "form": form,
    }
    return render(request, "accounts/login.html", context)


@login_required
def logout(request):
    auth_logout(request)
    return redirect("articles:reviews")


@login_required
def update(request):
    if request.method == "POST":
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("accounts:profile", request.user.pk)

    else:
        form = CustomUserChangeForm(instance=request.user)

    context = {
        "form": form,
    }
    return render(request, "accounts/update.html", context)


@login_required
def follow(request, pk):
    me = request.user
    user = get_user_model().objects.get(id=pk)
    if me.followings.filter(id=user.pk).exists():
        me.followings.remove(user)
        return redirect("accounts:profile", user.pk)
    else:
        if me == user:
            messages.warning(request, "자신은 팔로우 할 수 없습니다.")
            return redirect("accounts:profile", user.pk)
        else:
            me.followings.add(user)
            return redirect("accounts:profile", user.pk)


@login_required
def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect("accounts:profile")
    else:
        form = PasswordChangeForm(request.user)
    context = {
        "form": form,
    }
    return render(request, "accounts/update.html", context)

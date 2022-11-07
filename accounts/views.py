import requests
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


import secrets

state_token = secrets.token_urlsafe(16)


def kakao_request(request):
    kakao_api = "https://kauth.kakao.com/oauth/authorize?response_type=code"
    redirect_uri = "http://localhost:8000/accounts/login/kakao/callback"
    client_id = "e913455abcf98190d3d4f963e1cf9140"  # 배포시 보안적용 해야함
    return redirect(f"{kakao_api}&client_id={client_id}&redirect_uri={redirect_uri}")


def kakao_callback(request):
    data = {
        "grant_type": "authorization_code",
        "client_id": "e913455abcf98190d3d4f963e1cf9140",  # 배포시 보안적용 해야함
        "redirect_uri": "http://localhost:8000/accounts/login/kakao/callback",
        "code": request.GET.get("code"),
    }
    kakao_token_api = "https://kauth.kakao.com/oauth/token"
    access_token = requests.post(kakao_token_api, data=data).json()["access_token"]

    headers = {"Authorization": f"bearer ${access_token}"}
    kakao_user_api = "https://kapi.kakao.com/v2/user/me"
    kakao_user_information = requests.get(kakao_user_api, headers=headers).json()

    kakao_id = kakao_user_information["id"]
    kakao_nickname = kakao_user_information["properties"]["nickname"]
    # 유저 모델에 프로필 사진 추가시 사용
    kakao_profile_image = kakao_user_information["properties"]["profile_image"]

    if get_user_model().objects.filter(kakao_id=kakao_id).exists():
        kakao_user = get_user_model().objects.get(kakao_id=kakao_id)
    else:
        kakao_login_user = get_user_model()()
        kakao_login_user.username = kakao_nickname
        kakao_login_user.kakao_id = kakao_id
        kakao_login_user.profile_picture = kakao_profile_image
        kakao_login_user.set_password(str(state_token))
        kakao_login_user.save()
        kakao_user = get_user_model().objects.get(kakao_id=kakao_id)
    my_login(request, kakao_user)
    return redirect(request.GET.get("next") or "main:index")


def naver_request(request):
    naver_api = "https://nid.naver.com/oauth2.0/authorize?response_type=code"
    client_id = "rsgA7pxw8Rg9ZuAA0NAa"  # 배포시 보안적용 해야함
    redirect_uri = "http://localhost:8000/accounts/login/naver/callback"
    state_token = secrets.token_urlsafe(16)
    return redirect(
        f"{naver_api}&client_id={client_id}&redirect_uri={redirect_uri}&state={state_token}"
    )


def naver_callback(request):
    data = {
        "grant_type": "authorization_code",
        "client_id": "rsgA7pxw8Rg9ZuAA0NAa",  # 배포시 보안적용 해야함
        "client_secret": "9j7HPHbOuA",
        "code": request.GET.get("code"),
        "state": request.GET.get("state"),
        "redirect_uri": "http://localhost:8000/accounts/login/naver/callback",
    }
    naver_token_request_url = "https://nid.naver.com/oauth2.0/token"
    access_token = requests.post(naver_token_request_url, data=data).json()[
        "access_token"
    ]

    headers = {"Authorization": f"bearer {access_token}"}
    naver_call_user_api = "https://openapi.naver.com/v1/nid/me"
    naver_user_information = requests.get(naver_call_user_api, headers=headers).json()

    naver_id = naver_user_information["response"]["id"]
    naver_nickname = naver_user_information["response"]["nickname"]
    # 유저 모델에 프로필 사진 추가시 사용
    naver_profile_image = naver_user_information["response"]["profile_image"]

    if get_user_model().objects.filter(naver_id=naver_id).exists():
        naver_user = get_user_model().objects.get(naver_id=naver_id)
    else:
        naver_login_user = get_user_model()()
        naver_login_user.username = naver_nickname
        naver_login_user.naver_id = naver_id
        naver_login_user.profile_picture = naver_profile_image
        naver_login_user.set_password(str(state_token))
        naver_login_user.save()
        naver_user = get_user_model().objects.get(naver_id=naver_id)
    my_login(request, naver_user)

    return redirect(request.GET.get("next") or "main:index")


def google_request(request):
    google_api = "https://accounts.google.com/o/oauth2/v2/auth"
    client_id = "348547675760-crcb730t7v4ql8p107rc0j81343gblt6.apps.googleusercontent.com"  # 배포시 보안적용 해야함
    redirect_uri = "http://localhost:8000/accounts/login/google/callback"
    google_base_url = "https://www.googleapis.com/auth"
    google_email = "/userinfo.email"
    google_myinfo = "/userinfo.profile"
    scope = f"{google_base_url}{google_email}+{google_base_url}{google_myinfo}"
    return redirect(
        f"{google_api}?client_id={client_id}&response_type=code&redirect_uri={redirect_uri}&scope={scope}"
    )


def google_callback(request):
    data = {
        "code": request.GET.get("code"),
        "state": request.GET.get("state"),
        "grant_type": "authorization_code",
        "client_id": "348547675760-crcb730t7v4ql8p107rc0j81343gblt6.apps.googleusercontent.com",  # 배포시 보안적용 해야함
        "client_secret": "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",
        "redirect_uri": "http://localhost:8000/accounts/login/google/callback",
    }
    google_token_request_url = "https://oauth2.googleapis.com/token"
    access_token = requests.post(google_token_request_url, data=data).json()[
        "access_token"
    ]
    params = {
        "access_token": f"{access_token}",
    }
    google_call_user_api = "https://www.googleapis.com/oauth2/v3/userinfo"
    google_user_information = requests.get(google_call_user_api, params=params).json()

    googld_id = google_user_information["sub"]
    googld_name = google_user_information["name"]
    googld_email = google_user_information["email"]
    googld_picture = google_user_information["picture"]
    print(googld_id)
    if get_user_model().objects.filter(googld_id=googld_id).exists():
        google_user = get_user_model().objects.get(googld_id=googld_id)
    else:
        google_login_user = get_user_model()()
        google_login_user.username = googld_name
        google_login_user.email = googld_email
        google_login_user.profile_picture = googld_picture
        google_login_user.googld_id = googld_id
        google_login_user.set_password(str(state_token))
        google_login_user.save()
        google_user = get_user_model().objects.get(googld_id=googld_id)
    my_login(request, google_user)

    return redirect(request.GET.get("next") or "main:index")

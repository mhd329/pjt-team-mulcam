import os
import secrets
import requests
from .forms import (
    AuthForm,
    AddressForm,
    CustomUserChangeForm,
    CustomUserCreationForm,
    CustomPasswordChangeForm,
)
from random import randint
from .models import AuthPhone
from dotenv import load_dotenv
from django.http import JsonResponse
from pjt.settings import EMAIL_HOST_USER
from reviews.models import Study, Accepted
from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth import login as user_login
from django.contrib.auth import logout as user_logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import update_session_auth_hash
from django.utils.encoding import force_bytes, force_text
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect, get_object_or_404

from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode


# Create your views here.


# dotenv 참조 시크릿 키
load_dotenv()
# 카카오
KAKAO_CLIENT_ID = os.getenv("KAKAO_CLIENT_ID")
# 네이버
NAVER_CLIENT_ID = os.getenv("NAVER_CLIENT_ID")
NAVER_CLIENT_SECRET = os.getenv("NAVER_CLIENT_SECRET")
# 구글
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
# 깃허브
GITHUB_CLIENT_ID = os.getenv("GITHUB_CLIENT_ID")
GITHUB_CLIENT_SECRET = os.getenv("GITHUB_CLIENT_SECRET")

from reviews.models import Study, Accepted
from django.contrib import messages
from .models import User



# 소셜 로그인에 필요한 토큰 생성
state_token = secrets.token_urlsafe(32)

# 테스트용 html 페이지
def test(request):
    members = User.objects.all()
    users = get_user_model().objects.order_by("-id")
    context = {
        'members':members,
        "users": users,
    }
    return render(request, "accounts/test.html", context)


def social_login_request(request, service_name):
    google_base_url = "https://www.googleapis.com/auth"
    google_email = "/userinfo.email"
    google_myinfo = "/userinfo.profile"
    services = {
        "kakao": {
            "base_url": "https://kauth.kakao.com/oauth/authorize",
            "client_id": KAKAO_CLIENT_ID,
            "redirect_uri": "http://localhost:8000/accounts/login/kakao/callback",
            "response_type": "code",
        },
        "naver": {
            "base_url": "https://nid.naver.com/oauth2.0/authorize",
            "client_id": NAVER_CLIENT_ID,
            "redirect_uri": "http://localhost:8000/accounts/login/naver/callback",
            "response_type": "code",
            "state": state_token,
        },
        "google": {
            "base_url": "https://accounts.google.com/o/oauth2/v2/auth",
            "client_id": GOOGLE_CLIENT_ID,
            "redirect_uri": "http://localhost:8000/accounts/login/google/callback",
            "response_type": "code",
            "scope": f"{google_base_url}{google_email}+{google_base_url}{google_myinfo}",
        },
        "github": {
            "base_url": "https://github.com/login/oauth/authorize",
            "client_id": GITHUB_CLIENT_ID,
            "redirect_uri": "http://localhost:8000/accounts/login/github/callback",
            "scope": "read:user",
        },
    }
    for k, v in services[service_name].items():
        if k == "base_url":
            res = f"{v}?"
        else:
            res += f"{k}={v}&"
    return redirect(res)


def social_login_callback(request, service_name):
    services = {
        "kakao": {
            "data": {
                "grant_type": "authorization_code",
                "redirect_uri": "http://localhost:8000/accounts/login/kakao/callback",
                "client_id": KAKAO_CLIENT_ID,
                "code": request.GET.get("code"),
            },
            "api": "https://kauth.kakao.com/oauth/token",
            "user_api": "https://kapi.kakao.com/v2/user/me",
        },
        "naver": {
            "data": {
                "grant_type": "authorization_code",
                "redirect_uri": "http://localhost:8000/accounts/login/naver/callback",
                "client_id": NAVER_CLIENT_ID,
                "client_secret": NAVER_CLIENT_SECRET,
                "state": request.GET.get("state"),
                "code": request.GET.get("code"),
            },
            "api": "https://nid.naver.com/oauth2.0/token",
            "user_api": "https://openapi.naver.com/v1/nid/me",
        },
        "google": {
            "data": {
                "grant_type": "authorization_code",
                "redirect_uri": "http://localhost:8000/accounts/login/google/callback",
                "client_id": GOOGLE_CLIENT_ID,
                "client_secret": GOOGLE_CLIENT_SECRET,
                "state": request.GET.get("state"),
                "code": request.GET.get("code"),
            },
            "api": "https://oauth2.googleapis.com/token",
            "user_api": "https://www.googleapis.com/oauth2/v3/userinfo",
        },
        "github": {
            "data": {
                "redirect_uri": "http://localhost:8000/accounts/login/github/callback",
                "client_id": GITHUB_CLIENT_ID,
                "client_secret": GITHUB_CLIENT_SECRET,
                "code": request.GET.get("code"),
            },
            "api": "https://github.com/login/oauth/access_token",
            "user_api": "https://api.github.com/user",
        },
    }
    if service_name == "github":
        headers = {
            "accept": "application/json",
        }
        access_token = requests.post(
            services[service_name]["api"],
            data=services[service_name]["data"],
            headers=headers,
        ).json()["access_token"]
    else:
        access_token = requests.post(
            services[service_name]["api"], data=services[service_name]["data"]
        ).json()["access_token"]

    payload = {
        "kakao": {"Authorization": f"bearer ${access_token}"},
        "naver": {"Authorization": f"bearer {access_token}"},
        "google": {"access_token": f"{access_token}"},
        "github": {"Authorization": f"token {access_token}"},
    }

    if service_name == "google":
        params = payload[service_name]
        u_info = requests.get(services[service_name]["user_api"], params=params).json()
    else:
        headers = payload[service_name]
        u_info = requests.get(
            services[service_name]["user_api"], headers=headers
        ).json()
    if service_name == "kakao":
        login_data = {
            "kakao": {
                "social_id": u_info["id"],
                "username": u_info["properties"]["nickname"],
                "social_profile_picture": u_info["properties"]["profile_image"],
                "nickname": u_info["properties"]["nickname"],
                "email": u_info["kakao_account"]["email"]
                if "email" in u_info["kakao_account"]
                else "",
                "phone": None,
            },
        }
    elif service_name == "naver":
        login_data = {
            "naver": {
                "social_id": u_info["response"]["id"],
                "username": u_info["response"]["nickname"],
                "social_profile_picture": u_info["response"]["profile_image"]
                if "profile_image" in u_info["response"]
                else None,
                "nickname": u_info["response"]["name"]
                if "name" in u_info["response"]
                else None,
                "email": u_info["response"]["email"]
                if "email" in u_info["response"]
                else None,
                "phone": u_info["response"]["mobile"]
                if "mobile" in u_info["response"]
                else None,
            },
        }
    elif service_name == "google":
        login_data = {
            "google": {
                "social_id": u_info["sub"],
                "username": u_info["name"],
                "social_profile_picture": u_info["picture"]
                if u_info["picture"]
                else None,
                "nickname": u_info["name"] if u_info["name"] else None,
                "email": u_info["email"] if u_info["email"] else None,
                "phone": None,
            },
        }
    else:
        login_data = {
            "github": {
                "social_id": u_info["id"],
                "username": u_info["login"],
                "social_profile_picture": u_info["avatar_url"]
                if u_info["avatar_url"]
                else None,
                "nickname": u_info["bio"] if u_info["bio"] else None,
                "email": u_info["email"] if u_info["email"] else None,
                "phone": None,
                ### 깃허브에서만 가져오는 항목 ###
                "git_username": u_info["login"],
                ### 깃허브에서만 가져오는 항목 ###
            },
        }
    user_info = login_data[service_name]
    if get_user_model().objects.filter(social_id=user_info["social_id"]).exists():
        user = get_user_model().objects.get(social_id=user_info["social_id"])
        user.token = access_token
        user.save()
    else:
        user = get_user_model()()
        uid = user_info["social_id"]
        user.social_id = uid
        user.username = (
            user_info["username"]
            if service_name == "github"
            else f"{service_name}#{uid}"
        )
        user.social_profile_picture = user_info["social_profile_picture"]
        user.nickname = user_info["nickname"]
        user.email = user_info["email"]
        user.phone = user_info["phone"]
        user.set_password(str(state_token))
        user.is_social_account = True
        # 유저 토큰 가져오기
        user.token = access_token
        # 깃허브에서만 가져오는 항목
        user.git_username = u_info["login"] if service_name == "github" else None
        user.save()
        user = get_user_model().objects.get(social_id=user_info["social_id"])
    user_login(request, user)
    return redirect(request.GET.get("next") or "accounts:test")


def signup(request):
    if request.method == "POST":
        signup_form = CustomUserCreationForm(request.POST, request.FILES)
        address_form = AddressForm(request.POST)
        if signup_form.is_valid() and address_form.is_valid():
            user = signup_form.save(commit=False)
            # 주소
            user.address = request.POST["address"]
            user.detail_address = request.POST["detail_address"]
            # 휴대폰 번호
            if user.phone:
                user.phone = (
                    request.POST["phone"][:3]
                    + "-"
                    + request.POST["phone"][3:7]
                    + "-"
                    + request.POST["phone"][7:]
                )
            user.save()
            user_login(request, user)
            return redirect("accounts:test")
    else:
        signup_form = CustomUserCreationForm()
        signup_form.fields["phone"].widget.attrs["maxlength"] = 11
        address_form = AddressForm()
    context = {
        "signup_form": signup_form,
        "address_form": address_form,
    }
    return render(request, "accounts/signup.html", context)


@login_required
def update(request, user_pk):
    user = get_object_or_404(get_user_model(), pk=user_pk)
    if request.method == "POST":
        update_form = CustomUserChangeForm(request.POST, request.FILES, instance=user)
        address_form = AddressForm(request.POST, instance=user)
        auth_form = AuthForm(request.POST, instance=user)
        if update_form.is_valid() and address_form.is_valid() and auth_form.is_valid():
            user = update_form.save(commit=False)
            user.address = request.POST["address"]
            user.detail_address = request.POST["detail_address"]
            auth = auth_form.save(commit=False)
            # 휴대폰 번호
            if auth.phone:
                auth.phone = (
                    request.POST["phone"][:3]
                    + "-"
                    + request.POST["phone"][3:7]
                    + "-"
                    + request.POST["phone"][7:]
                )
            auth.save()
            user.save()
            return redirect("accounts:detail", user_pk)
    else:
        update_form = CustomUserChangeForm(instance=user)
        address_form = AddressForm(instance=user)
        if user.phone:
            phone = user.phone
            phone = "".join(phone.split("-"))
            user.phone = phone
        auth_form = AuthForm(instance=user)
        auth_form.fields["phone"].widget.attrs["maxlength"] = 11
    context = {
        "address_form": address_form,
        "update_form": update_form,
        "auth_form": auth_form,
        "user": user,
    }
    return render(request, "accounts/update.html", context)


def login(request):
    if request.method == "POST":
        login_form = AuthenticationForm(request, data=request.POST)
        if login_form.is_valid():
            user_login(request, login_form.get_user())
            return redirect(request.GET.get("next") or "reviews:index")
    else:
        login_form = AuthenticationForm()
    context = {
        "login_form": login_form,
    }
    return render(request, "accounts/login.html", context)


@login_required
def logout(request):
    user_logout(request)
    return redirect("accounts:test")


# test용도
def index(request):
    persons = get_user_model().objects.order_by("-pk")
    return render(
        request,
        "accounts/index.html",
        {
            "persons": persons,
        },
    )


def detail(request, user_pk):
    accepts = Accepted.objects.filter(users=user_pk).order_by("-pk")
    studies = []
    deactives = []
    
    for accept in accepts:
        if accept.joined:
            studies.append(accept.study)
    for study in studies:
        if not study.isactive:
            deactives.append(study)
    person = get_object_or_404(get_user_model(), pk=user_pk)
                 
    return render(
        request,
        "accounts/detail.html",
        {
            "person": person,
            "studies": studies,
            "deactives": deactives,
        },
    )

@login_required
def password_change(request, user_pk):
    user = get_object_or_404(get_user_model(), pk=user_pk)
    if request.method == "POST":
        pw_change_form = CustomPasswordChangeForm(user, request.POST)
        if pw_change_form.is_valid():
            user = pw_change_form.save()
            update_session_auth_hash(request, user)
            return redirect("accounts:detail", user_pk)
    else:
        pw_change_form = CustomPasswordChangeForm(user)
    context = {
        "pw_change_form": pw_change_form,
    }
    return render(request, "accounts/password.html", context)


def check(request, user_pk):
    today_ = str(datetime.date.today())
    user = get_object_or_404(get_user_model(), pk=user_pk)
    user_phone = request.POST["phone"]
    now_auth_phone = AuthPhone.objects.filter(phone=user_phone[1:])
    auth_count = 0
    for data in now_auth_phone:
        if data.created_at.strftime("%Y-%m-%d") == today_:
            auth_count += 1
            if auth_count == 5:
                break
    context = {
        "authCount": auth_count,
    }
    return JsonResponse(context)


# 휴대폰 인증번호 전송
def phone_auth(request, user_pk):
    user = get_object_or_404(get_user_model(), pk=user_pk)
    if user.phone:
        phone = user.phone
        phone = "".join(phone.split("-"))
        user.phone = phone
    random_auth_number = randint(1000, 10000)
    auth_phone = AuthPhone()
    auth_phone.phone = user.phone if user.phone else request.POST["phone"]
    auth_phone.auth_number = random_auth_number
    auth_phone.save()
    context = {}
    return JsonResponse(context)


import datetime
from django.utils import timezone


# 휴대폰 인증번호 입력 후 검증
def check_auth(request, user_pk):
    time_limit = timezone.now() + datetime.timedelta(minutes=5)
    user_phone = request.POST["phone"]
    phone_auth_number = int(request.POST["auth_number"])
    user = get_object_or_404(get_user_model(), pk=user_pk)
    now_auth_phone = AuthPhone.objects.filter(phone=user_phone[1:]).order_by(
        "-updated_at"
    )[0]
    if now_auth_phone.updated_at <= time_limit:
        if now_auth_phone.auth_number == phone_auth_number:
            user.phone = user_phone
            user.is_phone_active = True
            user.save()
            now_auth_phone.delete()
            is_phone_active = True
            auth_error_or_success = "인증 완료"
        else:
            is_phone_active = False
            auth_error_or_success = "인증 번호가 다릅니다."
    else:
        is_phone_active = False
        auth_error_or_success = "인증 시간이 만료되었습니다."
    context = {
        "isPhoneActive": is_phone_active,
        "authErrorOrSuccess": auth_error_or_success,
    }
    return JsonResponse(context)


# 이메일 인증 메일 생성
def active_mail(domain, uidb64, token):
    html_test = f"""\
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta http-equiv="X-UA-Compatible" content="IE=edge">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>CodeBee</title>
</head>
<body>    
<h1>[코드비 회원 인증]</h1>
<h3>아래 버튼을 클릭하면 인증이 완료됩니다.</h3>
<form action="http://{domain}/accounts/{uidb64}/{token}/">
<input type="submit" style="text-decoration: none; width: 100px; height: 40px; border-radius: 1rem;" value="인증하기">
</form>
</body>
</html>
"""
    return html_test


# 인증 메일 전송
def send_email(request, user_pk):
    user = get_object_or_404(get_user_model(), pk=user_pk)
    email_address = request.POST["email_address"]
    domain = get_current_site(request).domain
    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
    email_data = active_mail(domain, uidb64, state_token)
    email = EmailMultiAlternatives(
        "[코드비] 회원 이메일 인증", "", f"CodeBee <{EMAIL_HOST_USER}>", [email_address]
    )
    email.attach_alternative(email_data, "text/html")
    email.send()
    context = {
        "emailSendMessage": "메일이 도착하는데 시간이 다소 걸릴 수 있습니다.",
    }
    return JsonResponse(context)


# 인증 메일 확인
def check_email_auth(request, uidb64, token):
    user_pk = force_text(urlsafe_base64_decode(uidb64))
    user = get_object_or_404(get_user_model(), pk=user_pk)
    if token == state_token:
        user.is_email_active = True
        user.save()
        context = {
            "user": user,
        }
        return render(request, "accounts/email-auth.html", context)
    else:
        return render(request, "accounts/email-auth-failed.html")

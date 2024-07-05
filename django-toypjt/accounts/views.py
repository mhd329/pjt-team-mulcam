import json
import random
import smtplib
from datetime import datetime as dt
from django.contrib import messages
from email.message import EmailMessage
from config.settings import BASE_DIR
from .forms import UserPhoneNumberForm
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth import login as login_
from django.contrib.auth import logout as logout_
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import (
    CustomUserCreationForm,
    CustomUserChangeForm,
    CustomPasswordChangeForm,
)

# 사전 설정

EMAIL_ADDRESS_INFO = BASE_DIR / "mail.json"
with open(EMAIL_ADDRESS_INFO) as f:
    json_object = json.load(f)

smtp = smtplib.SMTP("smtp.gmail.com", 587)


greetings = [
    "안녕하세요.",
    "환영합니다!",
    "반갑습니다.",
    "반가워요!",
]
check_user_name = [
    "이름을 등록해주세요!",
    "아직 이름을 입력하지 않으셨네요!",
]
bye = [
    "안녕히가세요.",
    "잘가요!",
    "다음에 또 오세요!",
    "다음에 또 봐요!",
]
wd = [
    "당신이 그리울 거에요...",
    "다음에 또 오세요!",
]

# 뷰함수

# 회원가입


def signup(request):
    if request.user.username:
        messages.warning(request, "이미 가입 하셨군요!")
        return render(request, "400.html", status=400)
    else:
        if request.method == "POST":
            form = CustomUserCreationForm(request.POST)
            pn_form = UserPhoneNumberForm(request.POST)
            if form.is_valid() and pn_form.is_valid():
                user = form.save()
                user_phone_number = pn_form.save(commit=False)
                user_phone_number.user = user
                phone = user_phone_number.phone
                if phone:
                    p1 = "".join(phone[:3])
                    p2 = "".join(phone[3:7])
                    p3 = "".join(phone[7:])
                    phone = "-".join([p1, p2, p3])
                else:
                    pass
                user_phone_number.phone = phone
                user_phone_number.save()
                login_(request, user)
                g = random.choice(greetings)
                c = random.choice(check_user_name)
                if user.full_name:
                    messages.success(request, f"{user.full_name}님, {g}")
                else:
                    messages.success(request, f"익명의 사용자님, {g}")
                    messages.warning(request, f"{c}")
                return redirect("articles:reviews")
        else:
            form = CustomUserCreationForm()
            pn_form = UserPhoneNumberForm()
        context = {
            "form": form,
            "pn_form": pn_form,
        }
        return render(request, "accounts/form.html", context)


# 로그인
def login(request):
    if request.user.username:
        messages.warning(request, "이미 로그인 하셨군요!")
        return render(request, "400.html", status=400)
    else:
        if request.method == "POST":
            form = AuthenticationForm(request.POST, data=request.POST)
            if form.is_valid():
                login_(request, form.get_user())
                # 관리자 계정 활동내역 기록
                if request.user.is_superuser:
                    try:
                        now = dt.now()
                        smtp.ehlo()
                        smtp.starttls()
                        smtp.login(json_object["MY_ID"], json_object["MY_PASSWORD"])
                        msg = EmailMessage()
                        msg["Subject"] = "pjt02 관리자 계정으로 로그인 감지"
                        msg.set_content(
                            now.strftime(
                                "https://guarded-tundra-99188.herokuapp.com/articles/reviews/\n관리자 계정으로 로그인 되었습니다.\n일시 : %y.%m.%d %H:%M:%S"
                            )
                        )
                        msg["From"] = json_object["MY_ID"]
                        msg["To"] = (
                            get_user_model().objects.get(username="mhd329").email
                        )
                        smtp.send_message(msg)
                    except:
                        pass
                g = random.choice(greetings)
                c = random.choice(check_user_name)
                if form.get_user().full_name:
                    messages.error(request, f"{form.get_user().full_name}님, {g}")
                else:
                    messages.error(request, f"익명의 사용자님, {g}")
                    messages.warning(request, f"{c}")
                return redirect(request.GET.get("next") or "articles:reviews")
        else:
            form = AuthenticationForm()
        context = {
            "form": form,
        }
        return render(request, "accounts/login.html", context)


# 로그아웃
@login_required
def logout(request):
    b = random.choice(bye)
    if request.user.full_name:
        messages.error(request, f"{request.user.full_name}님, {b}")
    else:
        messages.error(request, f"익명의 사용자님, {b}")
    if request.user.is_superuser:
        try:
            now = dt.now()
            smtp.ehlo()
            smtp.starttls()
            smtp.login(json_object["MY_ID"], json_object["MY_PASSWORD"])
            msg = EmailMessage()
            msg["Subject"] = "관리자 계정 로그아웃 감지"
            msg.set_content(
                now.strftime(
                    "https://guarded-tundra-99188.herokuapp.com/articles/reviews/\n관리자 계정이 로그아웃 되었습니다.\n일시 : %y.%m.%d %H:%M:%S"
                )
            )
            msg["From"] = json_object["MY_ID"]
            msg["To"] = get_user_model().objects.get(username="admin").email
            smtp.send_message(msg)
        except:
            pass
    logout_(request)
    return redirect(request.META.get("HTTP_REFERER", "redirect_if_referer_not_found"))


# 회원정보조회
def detail(request, pk):
    now_user = request.user
    other_user = get_user_model().objects.get(id=pk)
    context = {
        "now_user": now_user,
        "other_user": other_user,
    }
    return render(request, "accounts/detail.html", context)


# 회원정보수정
@login_required
def update(request, pk):
    now_user = request.user
    other_user = get_user_model().objects.get(id=pk)
    if other_user.is_superuser:
        messages.error(request, "관리자 계정은 일반 페이지에서 수정이 불가능합니다.")
        messages.warning(request, "관리자 페이지를 이용해주세요.")
        return redirect("accounts:detail", other_user.pk)
    else:
        phone = other_user.userphonenumber
        if request.method == "POST":
            form = CustomUserChangeForm(request.POST, instance=other_user)
            pn_form = UserPhoneNumberForm(request.POST, instance=phone)
            if form.is_valid() and pn_form.is_valid():
                user = form.save()
                user_phone_number = pn_form.save(commit=False)
                user_phone_number.user = user
                phone = user_phone_number.phone
                if phone:
                    p1 = "".join(phone[:3])
                    p2 = "".join(phone[3:7])
                    p3 = "".join(phone[7:])
                    phone = "-".join([p1, p2, p3])
                    user_phone_number.phone = phone
                else:
                    pass
                user_phone_number.save()
                messages.success(request, "정보가 변경되었습니다.")
                return redirect("accounts:detail", other_user.pk)
        else:
            form = CustomUserChangeForm(instance=other_user)
            pn_form = UserPhoneNumberForm(instance=phone)
        context = {
            "form": form,
            "pn_form": pn_form,
            "now_user": now_user,
            "other_user": other_user,
        }
        return render(request, "accounts/form.html", context)


# 회원탈퇴
@login_required
def withdrawal(request, pk):
    user = get_user_model().objects.get(id=pk)
    if user.is_superuser:
        messages.error(request, "관리자 계정은 일반 페이지에서 탈퇴가 불가능합니다.")
        messages.warning(request, "관리자 페이지를 이용해주세요.")
        return redirect("accounts:detail", user.pk)
    else:
        w = random.choice(wd)
        b = random.choice(bye)
        if request.method == "POST":
            if user.full_name:
                messages.success(request, f"{user.full_name}! {w}")
            else:
                messages.success(request, f"{b}")
            user.delete()
            logout_(request)
            return redirect("articles:reviews")
        else:
            context = {
                "user": user,
            }
        return render(request, "accounts/withdrawal.html", context)


# 비밀번호 변경
@login_required
def change_pw(request, pk):
    user = request.user
    if request.method == "POST":
        form = CustomPasswordChangeForm(user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, "비밀번호가 변경되었습니다.")
            return redirect("accounts:detail", user.pk)
    else:
        form = CustomPasswordChangeForm(user)
    context = {
        "form": form,
        "user": user,
    }
    return render(request, "accounts/password.html", context)


# 에러 처리


def error_400(request, exception):
    return render(request, "400.html", status=400)


def error_403(request, exception):
    return render(request, "403.html", status=403)


def error_404(request, exception):
    return render(request, "404.html", status=404)


def error_500(request):
    return render(request, "500.html", status=500)

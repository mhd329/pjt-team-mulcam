import os
import secrets
import requests
from .forms import (
    AuthForm,
    AddressForm,
    SNSUserSignupForm,
    CustomUserChangeForm,
    CustomUserCreationForm,
    CustomPasswordChangeForm,
)
from random import randint
from dotenv import load_dotenv
from .models import AuthPhone, User
from django.http import JsonResponse
from pjt.settings import EMAIL_HOST_USER
from django.contrib.auth import get_user_model
from reviews.models import Study, Accepted, Honey
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


# 소셜 로그인에 필요한 토큰 생성
state_token = secrets.token_urlsafe(32)


# 테스트용 html 페이지
def test(request):
    members = User.objects.all()
    users = get_user_model().objects.order_by("-id")
    service_name = request.user.service_name if request.user.is_authenticated else None
    context = {
        "service_name": service_name,
        "members": members,
        "users": users,
    }
    return render(request, "accounts/test.html", context)


def social_signup_request(request):
    if "kakao" in request.path:
        service_name = "kakao"
    elif "google" in request.path:
        service_name = "google"
    elif "github" in request.path:
        service_name = "github"

    google_base_url = "https://www.googleapis.com/auth"
    google_email = "/userinfo.email"
    google_myinfo = "/userinfo.profile"

    services = {
        "kakao": {
            "base_url": "https://kauth.kakao.com/oauth/authorize",
            "client_id": KAKAO_CLIENT_ID,
            "redirect_uri": "http://codebee-env-1.eba-ybm4hjsv.ap-northeast-2.elasticbeanstalk.com/accounts/login/kakao/callback",
            "response_type": "code",
        },
        # "naver": {
        #     "base_url": "https://nid.naver.com/oauth2.0/authorize",
        #     "client_id": NAVER_CLIENT_ID,
        #     "redirect_uri": "http://localhost:8000/accounts/login/naver/callback",
        #     "response_type": "code",
        #     "state": state_token,
        # },
        "google": {
            "base_url": "https://accounts.google.com/o/oauth2/v2/auth",
            "client_id": GOOGLE_CLIENT_ID,
            "redirect_uri": "http://codebee-env-1.eba-ybm4hjsv.ap-northeast-2.elasticbeanstalk.com/accounts/login/google/callback",
            "response_type": "code",
            "scope": f"{google_base_url}{google_email}+{google_base_url}{google_myinfo}",
        },
        "github": {
            "base_url": "https://github.com/login/oauth/authorize",
            "client_id": GITHUB_CLIENT_ID,
            "redirect_uri": "http://codebee-env-1.eba-ybm4hjsv.ap-northeast-2.elasticbeanstalk.com/accounts/login/github/callback",
            "scope": "read:user",
        },
    }
    for k, v in services[service_name].items():
        if k == "base_url":
            res = f"{v}?"
        else:
            res += f"{k}={v}&"
    return redirect(res)


def social_signup_callback(request):
    if "kakao" in request.path:
        service_name = "kakao"
    elif "google" in request.path:
        service_name = "google"
    elif "github" in request.path:
        service_name = "github"
    services = {
        "kakao": {
            "data": {
                "grant_type": "authorization_code",
                "redirect_uri": "http://codebee-env-1.eba-ybm4hjsv.ap-northeast-2.elasticbeanstalk.com/accounts/login/kakao/callback",
                "client_id": KAKAO_CLIENT_ID,
                "code": request.GET.get("code"),
            },
            "api": "https://kauth.kakao.com/oauth/token",
            "user_api": "https://kapi.kakao.com/v2/user/me",
        },
        # "naver": {
        #     "data": {
        #         "grant_type": "authorization_code",
        #         "redirect_uri": "http://localhost:8000/accounts/login/naver/callback",
        #         "client_id": NAVER_CLIENT_ID,
        #         "client_secret": NAVER_CLIENT_SECRET,
        #         "state": request.GET.get("state"),
        #         "code": request.GET.get("code"),
        #     },
        #     "api": "https://nid.naver.com/oauth2.0/token",
        #     "user_api": "https://openapi.naver.com/v1/nid/me",
        # },
        "google": {
            "data": {
                "grant_type": "authorization_code",
                "redirect_uri": "http://codebee-env-1.eba-ybm4hjsv.ap-northeast-2.elasticbeanstalk.com/accounts/login/google/callback",
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
                "redirect_uri": "http://codebee-env-1.eba-ybm4hjsv.ap-northeast-2.elasticbeanstalk.com/accounts/login/github/callback",
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
        token = requests.post(
            services[service_name]["api"],
            data=services[service_name]["data"],
            headers=headers,
        ).json()
    else:
        token = requests.post(
            services[service_name]["api"], data=services[service_name]["data"]
        ).json()
    # ================================== 액세스 토큰 발급 ==================================
    access_token = token["access_token"]
    # ================================== 액세스 토큰 발급 ==================================
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
    print(
        u_info, 111111111111111111111111111111111111111111111111111111111111111111111111
    )
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
    # elif service_name == "naver":
    #     login_data = {
    #         "naver": {
    #             "social_id": u_info["response"]["id"],
    #             "username": u_info["response"]["nickname"],
    #             "social_profile_picture": u_info["response"]["profile_image"]
    #             "nickname": u_info["response"]["name"]
    #             "email": u_info["response"]["email"]
    #             "phone": u_info["response"]["mobile"]
    #         },
    #     }
    elif service_name == "google":
        login_data = {
            "google": {
                "social_id": u_info["sub"],
                "username": u_info["given_name"],
                "social_profile_picture": u_info["picture"]
                if "picture" in u_info
                else None,
                "nickname": u_info["given_name"],
                "email": u_info["email"],
                "phone": None,
            },
        }
    else:
        login_data = {
            "github": {
                "social_id": u_info["id"],
                "username": u_info["login"],
                "social_profile_picture": u_info["avatar_url"],
                "nickname": u_info["bio"],
                "email": u_info["email"],
                "phone": None,
                ### 깃허브에서만 가져오는 항목 ###
                "git_username": u_info["login"],
                ### 깃허브에서만 가져오는 항목 ###
            },
        }
    user_info = login_data[service_name]
    print(
        user_info,
        222222222222222222222222222222222222222222222222222222222222222222222222,
    )
    if get_user_model().objects.filter(social_id=user_info["social_id"]).exists():
        user = get_user_model().objects.get(social_id=user_info["social_id"])
        user_login(request, user)
        return redirect(request.GET.get("next") or "reviews:index")
    else:
        social_data = {
            # 소셜 서비스 구분
            "social_profile_picture": user_info["social_profile_picture"],
            "social_id": str(user_info["social_id"]),
            "service_name": service_name,
            "is_social_account": True,
            # 유저 토큰 가져오기
            "token": access_token,
        }
        data = {
            # 일반 정보
            "nickname": user_info["nickname"],
            "email": user_info["email"],
            "phone": user_info["phone"],
            # 깃허브에서만 가져오는 항목
            "git_username": (u_info["login"] if service_name == "github" else None),
        }
        signup_form = CustomUserCreationForm(initial=data)
        sns_signup_form = SNSUserSignupForm(initial=social_data)
        signup_form.fields["phone"].widget.attrs["maxlength"] = 11
        address_form = AddressForm()
        context = {
            "signup_form": signup_form,
            "address_form": address_form,
            "sns_signup_form": sns_signup_form,
        }
        return render(request, "accounts/signup.html", context)


# 소셜로그인 연결 끊기
def sns_logout(request, service_name):
    social_id = request.user.social_id
    user = get_object_or_404(get_user_model(), social_id=social_id)
    access_token = user.token
    if request.method == "POST":
        if request.user == user:
            services = {
                "kakao": {
                    "url": "https://kapi.kakao.com/v1/user/unlink",
                    "headers": {"Authorization": f"Bearer ${access_token}"},
                },
                "google": {
                    "url": "https://oauth2.googleapis.com/revoke",
                    "params": {"token": f"{access_token}"},
                },
            }
            data = "headers" if service_name == "kakao" else "params"
            try:
                requests.post(
                    services[service_name]["url"],
                    data=services[service_name][f"{data}"],
                )
                user.delete()
                context = {
                    "success": "success",
                    "msg": "정상적으로 해지되었습니다.",
                }
            except Exception:
                if service_name == "github":
                    context = {
                        "error_msg": "깃허브 계정 탈퇴는 관리자에게 문의해주세요.",
                    }
                else:
                    context = {
                        "error_msg": "에러가 발생했습니다.",
                    }
            return render(request, "accounts/sns-disconnect.html", context)
        else:
            return render(request, "accounts/access-error.html")
    else:
        context = {
            "user": user,
            "service_name": service_name,
        }
    return render(request, "accounts/sns-delete.html", context)


def signup(request):
    if request.method == "POST":
        signup_form = CustomUserCreationForm(request.POST, request.FILES)
        sns_signup_form = SNSUserSignupForm(request.POST)
        address_form = AddressForm(request.POST)
        if signup_form.is_valid() and address_form.is_valid():
            user = signup_form.save(commit=False)
            # 소셜 서비스 구분
            user.social_id = (
                request.POST["social_id"] if "social_id" in request.POST else None
            )
            user.service_name = (
                request.POST["service_name"] if "service_name" in request.POST else None
            )
            user.is_social_account = (
                True if "is_social_account" in request.POST else False
            )
            user.social_profile_picture = (
                request.POST["social_profile_picture"]
                if "social_profile_picture" in request.POST
                else None
            )
            # 유저 토큰
            user.token = request.POST["token"] if "token" in request.POST else None
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
            if user.is_social_account:
                return redirect("reviews:index")
            else:
                return redirect("accounts:cont")
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
    if request.user.pk == user_pk:
        user = get_object_or_404(get_user_model(), pk=user_pk)
        if request.method == "POST":
            update_form = CustomUserChangeForm(
                request.POST, request.FILES, instance=user
            )
            address_form = AddressForm(request.POST, instance=user)
            auth_form = AuthForm(request.POST, instance=user)
            if (
                update_form.is_valid()
                and address_form.is_valid()
                and auth_form.is_valid()
            ):
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
    else:
        messages.warning(request, "본인만 수정할 수 있습니다.")
        return redirect("reviews:index")


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
    return redirect("reviews:index")


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
    lang_list = ["Python", "Javascript", "Django", "Vue", "React"]
    # 유저 정보
    person = get_object_or_404(get_user_model(), pk=user_pk)
    accepts = Accepted.objects.filter(joined=True, users=person).order_by("-pk")
    plus = Honey.objects.filter(rated_user=person, like=True).count()
    minus = Honey.objects.filter(rated_user=person, dislike=True).count()
    honey = 15 + plus - minus
    profile_picture = person.profile_picture
    social_profile_picture = person.social_profile_picture
    if not len(accepts):
        return render(
            request,
            "accounts/detail.html",
            {
                "profile_picture": profile_picture,
                "social_profile_picture": social_profile_picture,
                "std_cnt": 0,
                "person": person,
                "honey": honey,
            },
        )
    else:
        # 유저가 참여했지만 리뷰를 작성하지 않은 스터디 목록
        partys = Accepted.objects.filter(
            joined=True, users=person, study__isactive=False
        )
        # print(deactive_study)
        # 유저가 참여한 모든 스터디(현재 진행 중인)
        ings = Accepted.objects.filter(joined=True, users=person, study__isactive=True)
        uncomment_study = []
        for party in partys:
            study = party.study
            if not study.comment_set.all().filter(user=person).exists():
                uncomment_study.append(study)
        # print(uncomment_study)

        deactives = []
        online = []
        offline = []
        for accept in accepts:
            if not accept.study.isactive:
                deactives.append(accept.study)
            if not accept.study.location_type:
                offline.append(accept.study)
            else:
                online.append(accept.study)

        # 유저가 참여한 스터디
        party = person.accepted_set.all().filter(joined=True)
        # print(party)
        studys = party.values("study")
        # print(studys)

        lan_dict = {}

        for study in studys:
            pk = study.get("study")
            study_ = Study.objects.get(pk=pk)
            lan_dict[study_.categorie] = lan_dict.get(study_.categorie, 0) + 1

        # print(lan_dict)
        val_ = list(lan_dict.values())
        most = max(val_)
        # print(most)

        langs = []
        for k, v in lan_dict.items():
            if v == most:
                langs.append(k)

        Std_cnt = Accepted.objects.filter(users_id=user_pk, joined=True).count()
        return render(
            request,
            "accounts/detail.html",
            context={
                "lang_list": lang_list,
                "accepts": accepts,
                "person": person,
                "ings": ings,
                "deactives": deactives,
                "honey": honey,
                "online": online,
                "offline": offline,
                "langs": langs,
                "partys": partys,
                "honey": honey,
                "std_cnt": Std_cnt,
                "uncomment_study": uncomment_study,
                "profile_picture": profile_picture,
                "social_profile_picture": social_profile_picture,
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
    user = get_object_or_404(get_user_model(), pk=user_pk)  # 지금은 사용하지 않음
    user_phone = request.POST["phone"]
    now_auth_phone = AuthPhone.objects.filter(
        phone=user_phone[
            1:
        ]  # AuthPhone 테이블에서 지금 요청한 휴대폰번호와 같은 번호를 가진 것들이 쿼리셋에 담겨져서 온다.
    )  # 필드가 int라서 맨 앞의 0이 생략된다.
    auth_count = 0  # 이 방법의 원리는,
    for data in now_auth_phone:  # 방금 가져온 그 쿼리셋 안에서,
        if (
            data.created_at.strftime("%Y-%m-%d") == today_
        ):  # 쿼리셋 안에 있는 어떤 데이터의 생성 날짜가 오늘과 같으면,
            auth_count += 1  # 1씩 올려주기
            if (
                auth_count == 5
            ):  # 그래서 다섯개, 즉 쿼리셋 내부의 모든 휴대폰 번호중에 '오늘'날짜를 가진 것들이 다섯 개 이상 되면 인증이 안된다.
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
    auth_phone.save()  # 여기서 세이브되면서 메세지 전송
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
def active_mail(domain, uidb64, token, email_address):
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
<form action="http://{domain}/accounts/{uidb64}/update/send-email/{token}/{email_address}/email-auth/">
<input type="submit" style="text-decoration: none; width: 7rem; height: 2rem; border-radius: 0.5rem;" value="인증하기">
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
    uemailb64 = urlsafe_base64_encode(force_bytes(email_address))
    email_data = active_mail(domain, uidb64, state_token, uemailb64)
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
def check_email_auth(request, uidb64, token, uemailb64):
    user_pk = force_text(urlsafe_base64_decode(uidb64))
    email_address = force_text(urlsafe_base64_decode(uemailb64))
    user = get_object_or_404(get_user_model(), pk=user_pk)
    if token == state_token:
        if user.is_email_active:
            context = {
                "error": "이미 인증된 유저입니다.",
            }
        else:
            user.email = email_address
            user.is_email_active = True
            user.save()
            context = {
                "success": "success",
                "msg": "인증이 완료되었습니다.",
            }
    else:
        context = {
            "error": "토큰 값이 다릅니다.",
        }
    return render(request, "accounts/email-auth.html", context)


def cont(request):
    return render(request, "accounts/cont.html")


@login_required
def delete(request, user_pk):
    user = get_object_or_404(get_user_model(), pk=user_pk)
    if request.method == "POST":
        if request.user == user:
            messages.success(request, "정상적으로 탈퇴 되었습니다.")
            user.delete()
            user_logout(request)
            return redirect("reviews:index")
        else:
            return render(request, "accounts/access-error.html")
    else:
        context = {
            "user": user,
        }
    return render(request, "accounts/delete.html", context)


@login_required
def follow(request, following_pk):
    user = get_object_or_404(get_user_model(), pk=following_pk)
    # 스스로를 팔로우하려는 경우
    if request.user == user:
        messages.warning(request, "스스로 팔로우 할 수 없습니다.")
        return redirect("accounts:detail", following_pk)
    # 팔로우하고 있는 상태인 경우
    if request.user in user.followers.all():
        user.followers.remove(request.user)
        is_followed = False
    # 팔로우하고 있지 않았을때
    else:
        user.followers.add(request.user)
        is_followed = True
    context = {
        "is_followed": is_followed,
        "followers_count": user.followers.count(),
        "followings_count": user.followings.count(),
    }
    return JsonResponse(context)

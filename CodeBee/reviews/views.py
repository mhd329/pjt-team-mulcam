from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import StudyForm, CommentForm, StudyDateForm, AcceptedForm, HoneyForm
from .models import Study, Comment, Accepted, StudyDate, Honey, Tag
from accounts.models import User
import requests
import json
from django.contrib import messages
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator

# Create your views here.
# 카카오톡 나에게 보내기 메시지 url
url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"
link_url = "http://codebee-env-1.eba-ybm4hjsv.ap-northeast-2.elasticbeanstalk.com"

def home(request):
    return render(request, "home.html")


def index(request):
    studies = Study.objects.order_by("-pk")
    fill = request.GET.get('fill')
    print(fill)
    if fill=='1':
        studies = Study.objects.filter(location_type=False).order_by("-pk")
    elif fill=='2':
        studies = Study.objects.filter(location_type=True).order_by("-pk")
    paginator = Paginator(studies, 16)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    context = {
        "studies": posts,
    }
    return render(request, "reviews/index.html", context)

@login_required
def create(request):
    if (request.user.is_phone_active) or request.user.is_social_account:
        if request.method == "POST":
            tag = ""
            temp = request.POST["tag"]
            if temp:
                tags = json.loads(temp)
                for t in tags:
                    tag += t["value"] + ","
                    try:
                        Tag(tag=t["value"]).save()
                    except:
                        pass
            print(request.POST["content"])
            study_form = StudyForm(request.POST, request.FILES)
            study_date = StudyDateForm(request.POST)
            if study_form.is_valid() and study_date.is_valid():
                study = study_form.save(commit=False)
                study.categorie = request.POST["categorie"]
                study.study_type = request.POST["study_type"]
                study.location_type = request.POST["location_type"]
                study.location = request.POST["location"]
                study.content = request.POST["content"]
                study.X = request.POST["X"]
                study.Y = request.POST["Y"]
                study.tag = tag
                study.host = request.user
                study.save()
                date = study_date.save(commit=False)
                date.study = study
                date.save()
                Aform = Accepted(joined=True, study=study, users=study.host)
                Aform.save()
                return redirect("reviews:index")
        else:
            tag = {
                "tags": [
                    "python",
                    "java",
                    "pug",
                    "react",
                    "vue",
                    "c++",
                    "sass",
                    "javascript",
                    "html",
                    "css",
                    "django",
                    "spring",
                    "ruby",
                ]
                + list(Tag.objects.all().values_list("tag", flat=True))
            }
            tagify = json.dumps(tag)
            study_form = StudyForm()
            study_date = StudyDateForm()
        context = {
            "tag": tagify,
            "study_form": study_form,
            "study_date": study_date,
        }
        return render(request, "reviews/form.html", context)
    else:
        messages.warning(request, '인증된 유저만 스터디 생성이 가능합니다.')
        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

def detail(request, study_pk):
    study = Study.objects.get(pk=study_pk)
    comment_form = CommentForm(request.POST)
    comments = Comment.objects.filter(study=study).order_by("-pk")
    reviewers = User.objects.filter(comment__study=study)
    if request.method =='POST':
        form = StudyDateForm(request.POST)
        if form.is_valid():
            temp = form.save(commit=False)
            temp.study = study
            temp.save()
            return redirect("reviews:detail", study_pk)
    dates = StudyDate.objects.filter(study_id=study_pk)
    form = StudyDateForm()
    cnt = len(Accepted.objects.filter(study=study))
    users = Accepted.objects.filter(study_id=study_pk)
    accepteduser = User.objects.filter(accepted__study_id=study_pk, accepted__joined=True)
    for user in users:
        if user.users == request.user:
            user_accepted = True
            break
    else:
        user_accepted = False
    context = {
        'accepteduser':accepteduser,
        'reviewers':reviewers,
        'comments':comments,
        'comment_form':comment_form,
        'reviews': study,
        'members': users,
        "form": form,
        "dates": dates,
        "study": study,
        "cnt": cnt,
        "check": user_accepted,
    }
    if study.isactive:
        return render(request, "reviews/detail.html", context)
    else:
        return render(request, "reviews/detail_deactive.html", context)


@login_required
def update(request, study_pk):
    study = Study.objects.get(pk=study_pk)
    date = StudyDate.objects.filter(study_id=study_pk)
    if study.isactive:
        if request.user == study.host:
            if request.method == "POST":
                tag = ""
                temp = request.POST["tag"]
                if temp:
                    tags = json.loads(temp)
                    for t in tags:
                        tag += t["value"] + ","
                study_form = StudyForm(request.POST, request.FILES, instance=study)
                study_date = StudyDateForm(request.POST, instance=date[0])
                if study_form.is_valid() and study_date.is_valid():
                    study = study_form.save(commit=False)
                    study.categorie = request.POST["categorie"]
                    study.study_type = request.POST["study_type"]
                    study.location_type = request.POST["location_type"]
                    study.location = request.POST["location"]
                    study.content = request.POST["content"]
                    study.X = request.POST["X"]
                    study.Y = request.POST["Y"]
                    study.tag = tag
                    study.host = request.user
                    study.save()
                    study_form.save()
                    date_ = study_date.save(commit=False)
                    date_.study = study
                    date_.save()
                    return redirect("reviews:detail", study_pk)
            else:
                tag = {'tags':["python","java","pug","react","vue","c++","sass","javascript","html","css","django","spring","ruby"] + list(Tag.objects.all().values_list('tag', flat=True))}
                tagify = json.dumps(tag)
                study_form = StudyForm(instance=study)
                study_date = StudyDateForm(instance=date[0])
                context = {
                    'tag': tagify,
                    'study': study,
                    'date': date,
                    'study_form': study_form,
                    'study_date': study_date,
                    }
                return render(request, 'reviews/form.html', context)
        else:
            return redirect("reviews:detail", study_pk)
    else:
        messages.warning(request, '잘못된 요청입니다.')
        return redirect("reviews:index")

@login_required
def delete(request, study_pk):
    study = Study.objects.get(pk=study_pk)
    if request.user == study.host:
        if study.isactive:
            study.delete()
    else:
        messages.warning(request, '권한이 없습니다.')
    return redirect("reviews:index")


@login_required
def join(request, study_pk, user_pk):
    study = Study.objects.get(pk=study_pk)
    accepted = Accepted.objects.filter(study_id=study_pk, joined=True)
    users = Accepted.objects.filter(users_id=user_pk)
    
    token = study.host.token
    if request.user.is_authenticated:
        if study.limits > len(accepted):
            for joined in users:
                if joined in accepted:
                    messages.warning(request, "이미 가입신청 한 그룹입니다.")
                    return redirect("reviews:detail", study_pk)
            else:
                Aform = Accepted(joined=False, study=study, users=request.user)
                Aform.save()
                accepted_now = Accepted.objects.filter(study_id=study_pk)
                if token:
                    try:
                        image_url = study.image.url
                        print('11111111111111111')
                    except:
                        image_url = "https://user-images.githubusercontent.com/108651809/201609398-060cbab1-1ff4-440f-a989-9ab77965eb94.png"
                    data = {
                        "template_object": json.dumps(
                            {
                                "object_type": "feed",
                                "content": {
                                    "title": f"{request.user}님의 스터디 가입신청! ({len(accepted_now)} / {study.limits})",
                                    "description": "신청을 승인해주세요!",
                                    "image_url": f"{image_url}",
                                    # "image_url": f"http://localhost:8000{image_url}",
                                    "image_width": 800,
                                    "image_height": 550,

                                    "link": {
                                        "web_url": link_url,
                                        "mobile_web_url": link_url,
                                        "android_execution_params": "contentId=100",
                                        "ios_execution_params": "contentId=100",
                                    },
                                },
                                "buttons": [
                                    {
                                        "title": "웹으로 이동",
                                        "link": {
                                            "web_url": link_url,
                                            "mobile_web_url": link_url,
                                        },
                                    },
                                    {
                                        "title": "앱으로 이동",
                                        "link": {
                                            "android_execution_params": "contentId=100",
                                            "ios_execution_params": "contentId=100",
                                        },
                                    },
                                ],
                            }
                        )
                    }
                    headers = {"Authorization": "Bearer " + token}
                    response = requests.post(url, headers=headers, data=data)
                    print(str(response.json()))
                messages.success(request, "가입 신청이 완료되었습니다. 호스트의 승인을 기다려 주세요.")
                return redirect("reviews:detail", study_pk)
        else:
            messages.success(request, "모집인원이 가득 찬 그룹입니다.")
            return redirect("reviews:detail", study_pk)
    else:
        pass

@login_required
def study_accepted(request, study_id, users_id):
    study = Study.objects.get(id=study_id)
    user = User.objects.get(id=users_id)
    aform = Accepted.objects.get(users=user, study=study)
    if study.isactive:
        if request.user == study.host:
            aform.joined = True
            aform.save()
            return redirect("reviews:detail", study_id)
        else:
            return redirect("reviews:detail", study_id)
    else:
        return redirect("reviews:index")


@login_required
def study_kick(request, study_id, users_id):
    study = Study.objects.get(id=study_id)
    user = User.objects.get(id=users_id)
    aform = Accepted.objects.get(users=user, study=study)
    token = user.token
    if study.isactive:
        if request.user == study.host and user != study.host:
            aform.delete()
            if token:
                try:
                    image_url = study.image.url
                except:
                    image_url = "https://user-images.githubusercontent.com/108651809/201609398-060cbab1-1ff4-440f-a989-9ab77965eb94.png"
                data = {
                    "template_object": json.dumps(
                        {
                            "object_type": "feed",
                            "content": {
                                "title": f"{user.fullname}님의 스터디 가입신청이 거부되었습니다.",
                                "description": "다른 스터디에 참여해보세요!",
                                "image_url": f"{image_url}",
                                "image_width": 800,
                                "image_height": 550,
                                "link": {
                                    "web_url": link_url,
                                    "mobile_web_url": link_url,
                                    "android_execution_params": "contentId=100",
                                    "ios_execution_params": "contentId=100",
                                },
                            },
                            "buttons": [
                                {
                                    "title": "웹으로 이동",
                                    "link": {
                                        "web_url": link_url,
                                        "mobile_web_url": link_url,
                                    },
                                },
                                {
                                    "title": "앱으로 이동",
                                    "link": {
                                        "android_execution_params": "contentId=100",
                                        "ios_execution_params": "contentId=100",
                                    },
                                },
                            ],
                        }
                    )
                }
                headers = {"Authorization": "Bearer " + token}
                response = requests.post(url, headers=headers, data=data)
                print(str(response.json()))
            return redirect("reviews:detail", study_id)
        elif request.user == user and user != study.host:
            aform.delete()
            return redirect("reviews:detail", study_id)
        else:
            return redirect("reviews:detail", study_id)
    return redirect("reviews:index")


@login_required
def gathering(request, study_pk):
    accepted = Accepted.objects.filter(study_id=study_pk, joined=1)
    study = Study.objects.get(pk=study_pk)
    message = request.POST["message"]
    if request.user == study.host:
        try:
            image_url = study.image.url
        except:
            image_url = "https://user-images.githubusercontent.com/108651809/201609398-060cbab1-1ff4-440f-a989-9ab77965eb94.png"
        data = {
            "template_object": json.dumps(
                {
                    "object_type": "feed",
                    "content": {
                        "title": f"{request.user}님의 메시지",
                        "description": f"{message}",
                        "image_url": image_url,
                        # "image_url": f"{link_url}{image_url}",
                        "image_width": 800,
                        "image_height": 550,
                        "link": {
                            "web_url": link_url,
                            "mobile_web_url": link_url,
                            "android_execution_params": "contentId=100",
                            "ios_execution_params": "contentId=100",
                        },
                    },
                    "buttons": [
                        {
                            "title": "웹으로 이동",
                            "link": {
                                "web_url": link_url,
                                "mobile_web_url": link_url,
                            },
                        },
                        {
                            "title": "앱으로 이동",
                            "link": {
                                "android_execution_params": "contentId=100",
                                "ios_execution_params": "contentId=100",
                            },
                        },
                    ],
                }
            )
        }
        for user in accepted:
            token = user.users.token
            if token:
                headers = {"Authorization": "Bearer " + token}
                response = requests.post(url, headers=headers, data=data)
                print(str(response.json()))
                messages.success(request, "메시지 전송이 완료되었습니다.")
            else:
                print("no")
        return redirect("reviews:detail", study_pk)
    else:
        return redirect("reivews:index")


# ==================================comment=======================


def done(request, study_pk):
    study = Study.objects.get(pk=study_pk)
    if request.user == study.host:
        study.isactive = False
        study.save()
    else:
        messages.warning(request, '권한이 없습니다.')
    return redirect("reviews:detail", study_pk)


def review(request, study_id):
    study = Study.objects.filter(pk=study_id)
    comments = Comment.objects.all().order_by("-pk")
    comment_form = CommentForm()
    context = {
        "reviews": study,
        "comment_form": comment_form,
        "comments": comments,
    }
    return render(request, "reviews/review.html", context)


@login_required
def comment_create(request, pk):
    accepted = Accepted.objects.filter(study_id=pk, users=request.user)
    if accepted.exists() and not Comment.objects.filter(study_id=pk, user=request.user).exists():
        review = get_object_or_404(Study, pk=pk)
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.study_id = review.id
            comment.user = request.user
            comment.save()
            return redirect('reviews:detail', pk)
    else:
        messages.warning(request,'한개의 스터디에 한개의 리뷰만 남길 수 있습니다.')
        return redirect('reviews:detail', pk)

@login_required
def comment_update(request, pk, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)
    if request.user == comment.user:
        jsonObject = json.loads(request.body)
        comment.content = jsonObject.get("content")
        comment.save()
        upcomment = Comment.objects.get(pk=comment_pk)
        context = {
            "comments_date": upcomment.updated_at,
        }
        return JsonResponse(context)
    else:
        messages.warning(request,'잘못된 요청입니다.')
        return redirect('reviews:detail', pk)
@login_required
def comment_delete(request, pk, comment_pk):
    if request.user.is_authenticated:
        comment = Comment.objects.get(pk=comment_pk)
        comment.delete()

        comments = Comment.objects.filter(study_id=pk).order_by("-pk")
        comments_data = []
        for co in comments:
            co.created_at = co.created_at.strftime("%Y-%m-%d %H:%M")
            comments_data.append(
                {
                    "request_user_pk": request.user.pk,
                    "comment_pk": co.pk,
                    "user_pk": co.user.pk,
                    "username": co.user.username,
                    "content": co.content,
                    "created_at": co.created_at,
                    "updated_at": co.updated_at,
                    "study_id": co.study_id,
                }
            )
        context = {"comments_data": comments_data}
        return JsonResponse(context)


# Google Calendar Test
def test_calendar(request):

    return render(request, "reviews/test.html")


# 콜
def google_call(request):
    # if request.user.g_token:
    #     return render(request, 'reviews/test.html')
    # else:
    #     url = 'https://accounts.google.com/o/oauth2/v2/auth?client_id=503216611677-ah2v4o4cuqsustpbkvtot6ukdah6dhfp.apps.googleusercontent.com&redirect_uri=http://localhost:8000/reviews/google_code&response_type=code&scope=https://www.googleapis.com/auth/calendar'
    #     return redirect(url)
    url = "https://accounts.google.com/o/oauth2/v2/auth?client_id=503216611677-ah2v4o4cuqsustpbkvtot6ukdah6dhfp.apps.googleusercontent.com&redirect_uri=http://localhost:8000/reviews/google_code&response_type=code&scope=https://www.googleapis.com/auth/calendar"
    return redirect(url)


# 콜백
def google_code(request):
    url = "https://oauth2.googleapis.com/token"
    data = {
        "grant_type": "authorization_code",
        "redirect_uri": "http://localhost:8000/reviews/google_code",
        "client_id": "503216611677-ah2v4o4cuqsustpbkvtot6ukdah6dhfp.apps.googleusercontent.com",  # 배포시 보안적용 해야함
        "client_secret": "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",  # 배포시 보안적용 해야함
        "project_id": "keen-button-368611",
        "state": request.GET.get("state"),
        "code": request.GET.get("code"),
    }
    res = requests.post(url, data=data).json()
    token = res["access_token"]
    re_token = res["refresh_token"]
    print(token)
    user_ = get_user_model().objects.get(pk=request.user.pk)
    user_.g_token = token
    user_.save()
    url = "https://www.googleapis.com/calendar/v3/calendars/primary/events?sendUpdates=none&key=AIzaSyB86Erv475UlH5VfgBaSCA53hPcnoR46IA"
    headers = {
        "Authorization": "Bearer" + token,
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
    # data = {
    #     "end":{
    #         "dateTime":schedule.study_end.strftime("%Y-%m-%dT%H:%M:%S"),
    #         "timeZone":"Asia/Seoul"
    #     },
    #     "start":{
    #         "dateTime":schedule.study_at.strftime("%Y-%m-%dT%H:%M:%S"),
    #         "timeZone":"Asia/Seoul"
    #     },
    #     "summary": study.title,
    #     "location":study.location,
    #     "description": study.content
    # }
    data = {
        "end": {"dateTime": "2022-11-18T13:00:00", "timeZone": "Asia/Seoul"},
        "start": {"dateTime": "2022-11-18T13:00:00", "timeZone": "Asia/Seoul"},
        "summary": "test",
        "location": "test",
        "description": "test",
    }

    response = requests.post(url, headers=headers, data=data)
    if response.json().get("code") == 200:
        print("일정이 성공적으로 등록되었습니다.")
    else:
        print("일정이 성공적으로 등록되지 못했습니다. 오류메시지 : " + str(response.json()))
    return redirect("reviews:test_calendar")


def likes(request, study_pk, user_pk):
    study = get_object_or_404(Study, pk=study_pk)
    rated = get_object_or_404(get_user_model(), pk=user_pk)
    rating = get_object_or_404(get_user_model(), pk=request.user.pk)
    check = Honey.objects.filter(study=study, rating_user=rating, rated_user=rated).exists()
    join_user = Accepted.objects.filter(study=study, users=rating, joined=True).exists()
    print(rated)
    if rated == request.user:
        messages.warning(request, "본인을 평가할 수 없습니다.")

    elif not join_user:
        messages.warning(request, "스터디 참가자들만 평가 가능합니다.")

    else:
        if check:
            honey = Honey.objects.get(study=study, rating_user=rating, rated_user=rated)
            if honey.like == True:
                honey.delete()
            else:
                honey.dislike = False
                honey.like = True
                honey.save()
        else:
            honeyform = HoneyForm(request)
            honey = honeyform.save(commit=False)
            honey.study = study
            honey.rating_user = rating
            honey.rated_user = rated
            honey.like = True
            honey.save()

    return redirect("reviews:detail", study_pk)


def dislikes(request, study_pk, user_pk):
    study = get_object_or_404(Study, pk=study_pk)
    rated = get_object_or_404(get_user_model(), pk=user_pk)
    rating = get_object_or_404(get_user_model(), pk=request.user.pk)
    check = Honey.objects.filter(
        study=study, rating_user=rating, rated_user=rated).exists()
    join_user = Accepted.objects.filter(study=study, users=rating, joined=True).exists()

    if rated == request.user:
        messages.warning(request, "본인을 평가할 수 없습니다.")

    elif not join_user:
        messages.warning(request, "스터디 참가자들만 평가 가능합니다.")

    else:
        if check:
            honey = Honey.objects.get(study=study, rating_user=rating, rated_user=rated)
            if honey.dislike == True:
                honey.delete()
            else:
                honey.dislike = True
                honey.like = False
                honey.save()
        else:
            honeyform = HoneyForm(request)
            honey = honeyform.save(commit=False)
            honey.study = study
            honey.rating_user = rating
            honey.rated_user = rated
            honey.dislike = True
            honey.save()

    return redirect("reviews:detail", study_pk)


def del_date(request, date_pk):
    date = StudyDate.objects.get(pk=date_pk)
    date.delete()
    return JsonResponse({})


def search(request):
    search = request.GET.get("search")
    field = request.GET.get("field")
    if field == "1" or not field:
        studies = (Study.objects.filter(host__username__contains=search)
            or Study.objects.filter(tag__icontains=search)
            or Study.objects.filter(title__contains=search)
            or Study.objects.filter(categorie__contains=search)
        ).order_by('-pk')
        studies = list(set(studies))
    elif field == "2":
        studies = Study.objects.filter(title__icontains=search).order_by('-pk')
    elif field == "3":
        studies = Study.objects.filter(host__username__contains=search).order_by('-pk')

    elif field == "4":
        studies = Study.objects.filter(categorie__icontains=search).order_by('-pk')
    elif field == "5":
        studies = Study.objects.filter(tag__icontains=search).order_by('-pk')
    elif field == "6":
        studies = Study.objects.filter(location__icontains=search).order_by('-pk')
    page = request.GET.get('page', '1') 
    paginator = Paginator(studies, 16)
    posts = paginator.get_page(page)
    context = {
        'posts':posts,
        'field': field,
        'searched':search,
    }
    return render(request, "reviews/search.html", context)
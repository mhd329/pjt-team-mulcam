from django.shortcuts import render, redirect
from articles.models import Article
from search.models import Search
from reviews.models import Review
from django.db.models import Avg

# Create your views here.


def index(request):
    # 모든 아티클 + 평균평점
    all_article = Article.objects.annotate(gra=Avg("review__grade"))
    all_grade = []
    for article in all_article:
        g = article.gra
        if g is None:
            all_grade.append(0)
        else:
            all_grade.append(g * 20)
    all_articles = zip(all_article, all_grade)
    # 캐러셀 + 평균평점
    carousel_articles = Article.objects.order_by("-pk")[:3].annotate(
        gra=Avg("review__grade")
    )
    carousel_grade = []
    for carousel in carousel_articles:
        c = carousel.gra
        if c is None:
            carousel_grade.append(0)
        else:
            carousel_grade.append(carousel.gra * 20)

    carousel = zip(carousel_articles, carousel_grade)
    hot_keyword = Search.objects.all().order_by("-count")[:5]

    # for article in carousel_articles:
    #     reviews = Review.objects.filter(article_id=article.pk)
    #     grade_list = []
    #     for g in reviews:
    #         grade_list.append(g.grade)
    #     if len(grade_list) > 1:
    #         grade = round(sum(grade_list) / len(grade_list), 1)
    #         send_grade_ = (grade) * 20
    #         grades.append(send_grade_)

    context = {
        "carousel_articles": carousel,
        "all_article": all_articles,
        "hot_keyword": hot_keyword,
    }
    return render(request, "main/index.html", context)


def theme(request, pk):
    if pk == 1:
        theme = "산"
    elif pk == 2:
        theme = "강"
    elif pk == 3:
        theme = "바다"
    elif pk == 4:
        theme = "도심"
    filter_article = Article.objects.filter(camp_type__contains=theme)

    context = {
        "filter_article": filter_article,
        "theme": theme,
    }

    return render(request, "main/theme.html", context)


def all(request):
    all_article = Article.objects.all()

    context = {
        "all_article": all_article,
    }

    return render(request, "main/all.html", context)


def first(request):

    return render(request, "main/first.html")


# def map_filter(request,pk):
#     return red

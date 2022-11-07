from django.shortcuts import render, redirect
from articles.models import Article
from django.db.models import Q
from .models import Search
from reviews.models import Review

# Create your views here.

# 비동기 모달로 보내기 아티클 작성페이지
def article_search(request):
    search = request.GET.get("search", "")
    all_article = Article.objects.all()

    if search:
        search_data = all_article.filter(Q(contact__icontains=search))

        if len(search) == 0:
            none_info = "공백을 입력하셨습니다."
            context = {
                "none_info": none_info,
            }

        elif len(search_data) == 0:
            none_info = "검색 결과가 없습니다."
            context = {
                "none_info": none_info,
            }
        else:
            context = {"search_data": search_data}

        return redirect("main:index", context)


def search(request):
    search = request.GET.get("q", "")
    all_article = Article.objects.all()
    all_review = Review.objects.all()
    if search:
        search_article = all_article.filter(Q(name__icontains=search))
        search_review = all_review.filter(Q(title__icontains=search))
    if len(search) == 0:
        none_info = "공백을 입력하셨습니다."
        context = {"none_info": none_info, "search": search}
        return render(request, "search/search_list.html", context)

    elif len(search_article) + len(search_review) == 0:
        none_info = "검색 결과가 없습니다."
        context = {"none_info": none_info, "search": search}
        return render(request, "search/search_list.html", context)

    elif len(search) > 0:
        if Search.objects.filter(keyword=search):
            search_keyword = Search.objects.get(keyword=search)
            search_keyword.count += 1
            search_keyword.save()
        else:
            Search.objects.create(keyword=search, count=1)
        context = {
            "search_article": search_article,
            "search_review": search_review,
            "search": search,
        }
    return render(request, "search/search_list.html", context)


def k_map(request, pk):
    if pk == 1:
        localmap = "경기도"
    elif pk == 2:
        localmap = "강원도"
    elif pk == 3:
        localmap = "충청도"
    elif pk == 4:
        localmap = "경상도"
    elif pk == 5:
        localmap = "전라도"
    elif pk == 6:
        localmap = "제주도"

    local_list = Article.objects.filter(local=pk)
    print(local_list)
    context = {
        "search_article": local_list,
        "localmap": localmap,
    }

    return render(request, "search/search_list.html", context)

from django.shortcuts import render, redirect
from articles.models import Article
from django.db.models import Q

# Create your views here.


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

    # 비동기 모달로 보내기 아티클 작성페이지


def search(request):
    search = request.GET.get("search", "")
    all_article = Article.objects.all()
    if search:
        search_data = all_article.filter(Q(contact__icontains=search))

    if len(search) > 0:
        context = {
            "search_data": search_data,
        }
        return render(request, "search/search_list.html", context)
    elif len(search) == 0:
        none_info = "공백을 입력하셨습니다."
        context = {
            "none_info": none_info,
        }
        return render(request, "search/search_list.html", context)
    elif len(search_data) == 0:
        none_info = "검색 결과가 없습니다."
        context = {
            "none_info": none_info,
        }
        return render(request, "search/search_list.html", context)

from django.shortcuts import render, redirect
from .models import Review

# Create your views here.
def index(request):

    review_data = Review.objects.order_by("id")
    context = {"review_data": review_data}

    return render(request, "index.html", context)


def new(request):
    return render(request, "new.html")


def create(request):
    title = request.GET.get("title")
    content = request.GET.get("content")

    review = Review()
    review.title = title
    review.content = content
    review.save()

    return redirect("review:index")


def detail(request, pk):
    review_data = Review.objects.get(id=pk)
    context = {
        "review_data": review_data,
    }

    return render(request, "detail.html", context)


def edit(request, pk):
    review_data = Review.objects.get(id=pk)
    context = {
        "review_data": review_data,
    }

    return render(request, "edit.html", context)


def update(request, pk):
    title = request.GET.get("title")
    content = request.GET.get("content")
    review_data = Review.objects.get(id=pk)
    review_data.title = title
    review_data.content = content
    # save() 되면 auto_now 로 인해 자동으로 현재 시간으로 갱신됨
    review_data.save()
    context = {
        "review_data": review_data,
    }

    return render(request, "detail.html", context)


def delete(request, pk):
    review_data = Review.objects.get(id=pk)
    review_data.delete()

    return redirect("review:index")


def search_title(request):
    review_title = request.GET.get("searchTitle")
    retrieved_review_data = Review.objects.filter(title__icontains=review_title)
    context = {
        "retrieved_review_data": retrieved_review_data,
    }

    return render(request, "search.html", context)

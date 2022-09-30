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


def detail(request, pk_):
    review_data = Review.objects.get(pk=pk_)
    context = {"review_data": review_data}

    return render(request, "detail.html", context)


def edit(request, pk_):
    review_data = Review.objects.get(pk=pk_)
    context = {
        "review_data": review_data,
    }

    return render(request, "edit.html", context)


def update(request, pk_):
    title = request.GET.get("title")
    content = request.GET.get("content")
    review_data = Review.objects.get(pk=pk_)
    review_data.title = title
    review_data.content = content
    review_data.save()
    context = {
        "review_data": review_data,
    }

    return redirect("review:index")
    url = "detail/" + str(pk_)

    return render(request, url, context)


def delete(request, pk_):
    review_data = Review.objects.get(pk=pk_)
    review_data.delete()

    return redirect("review:index")

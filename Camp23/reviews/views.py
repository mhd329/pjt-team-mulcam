from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .form import CreateReview
from articles.models import Article
from .models import Review


# Create your views here.


def review_list(request):
    all_reviews = Review.objects.all()

    context = {
        "all_reviews": all_reviews,
    }
    return render(request, "reviews/review_list.html", context)


@login_required
def create(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    if request.method == "POST":
        form = CreateReview(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.article = article
            review.user = request.user
            review.save()
            return redirect("articles:detail", article_pk)
    else:
        form = CreateReview()
    context = {"form": form}
    return render(request, "reviews/create.html", context)


def detail(request, review_pk):
    pick_review = get_object_or_404(Review, pk=review_pk)
    grade = round(pick_review.grade, 1)
    send_grade = f"width:{(grade)*20}%;"
    context = {
        "pick_review": pick_review,
        "send_grade": send_grade,
    }
    return render(request, "reviews/detail.html", context)


@login_required
def update(request, review_pk):
    pick_review = get_object_or_404(Review, pk=review_pk)
    if request.method == "POST":
        form = CreateReview(request.POST, instance=pick_review)
        if form.is_valid():
            form.save()
            return redirect("reviews:detail", review_pk)
    else:
        form = CreateReview(instance=pick_review)
    context = {
        "form": form,
        "pick_user": pick_review,
    }
    return render(request, "reviews/update.html", context)


@login_required
def delete(request, review_pk):
    pick_review = Review.objects.get(pk=review_pk)
    if request.user == pick_review.user:
        pick_review.delete()
    return redirect("reviews:review_list")

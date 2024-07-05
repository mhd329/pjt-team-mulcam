from django.shortcuts import render, redirect
from .models import Review
from .forms import ReviewForm
from django.contrib.auth.decorators import login_required
from accounts.models import User
from django.db.models import Q

# Create your views here.
def index(request):
    reviews = Review.objects.order_by("-id")
    context = {
        "reviews": reviews,
    }
    return render(request, "articles/index.html", context)


@login_required
def create(request):
    if request.method == "POST":
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.user = request.user
            review.user_name = User.objects.get(pk=request.user.pk)
            review.save()
            return redirect("articles:index")
    else:
        review_form = ReviewForm()
    context = {
        "review_form": review_form,
    }
    return render(request, "articles/create.html", context=context)


def detail(request, pk):
    review = Review.objects.get(pk=pk)
    context = {
        "review": review,
    }
    return render(request, "articles/detail.html", context)


@login_required
def delete(request, pk):
    review = Review.objects.get(pk=pk)
    if request.user == review.user:
        review.delete()
        return redirect("articles:index")
    return redirect("articles:detail", review.pk)


@login_required
def update(request, pk):
    review = Review.objects.get(pk=pk)
    if request.user == review.user:
        if request.method == "POST":
            review_form = ReviewForm(request.POST, instance=review)
            if review_form.is_valid():
                review_form.save()
                return redirect("articles:detail", review.pk)
        else:
            review_form = ReviewForm(instance=review)
    else:
        return redirect("articles:index")
    context = {
        "review_form": review_form,
    }
    return render(request, "articles/update.html", context)

def search(request):
    if request.method == 'POST':
        searched = request.POST['searched']
        users = User.objects.filter(username__contains=searched)
        reviews = Review.objects.filter(Q(title__contains=searched) | Q(content__contains=searched) | Q(movie_name__contains=searched))
        context = {'searched' : searched, 'users': users, 'reviews' : reviews}
        return render(request, 'articles/search.html', context)
    else:
        return redirect('articles:index')

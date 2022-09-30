from django.shortcuts import render, redirect
from .models import Review

# Create your views here.
def index(request):

    review_data = Review.objects.order_by('id')
    context = {"review_data": review_data}

    return render(request, "index.html", context)

def new(request):
    return render(request, "new.html")

def create(request):
    title = request.GET.get("title")
    content = request.GET.get("content")

    Review.objects.create(title=title, content=content)

    return redirect("review:index")

def detail(request, pk_):
    review_data = Review.objects.get(pk=pk_)
    context ={'review_data' : review_data}
    
    return render(request, "detail.html", context)

def edit(request, pk_):
    review_data = Review.objects.get(pk=pk_)

    return render(request, "edit.html")

def delete(request, pk_):
    review_data = Review.objects.get(pk=pk_)
    
    return redirect("index.html")

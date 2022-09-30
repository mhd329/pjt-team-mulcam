from django.shortcuts import render, redirect
from .models import Review

# Create your views here.
def index(request):

    temp = Review.objects.all()
    context = {"temp": temp}

    return render(request, "index.html", context)


def new(request):
    return render(request, "new.html")


def edit(request, pk):
    return render(request, "edit.html")


def delete(request, pk):
    return redirect("index.html")

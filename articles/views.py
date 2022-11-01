from django.shortcuts import render

# Create your views here.
def camp01(request):
    return render(request, "articles/camp01.html")

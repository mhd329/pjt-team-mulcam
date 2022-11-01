from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import get_user_model,login as my_login, logout as my_logout
from django.contrib.auth.decorators import login_required
from .form import CreateUserForm,ChangeUserInfo
from django.contrib.auth.forms import AuthenticationForm

# Create your views here.

def signup(request):
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user= form.save()
            my_login(request, user)
            return redirect ("main:index")
    else:
        form = CreateUserForm()
    context= {
        'form':form
    }
    return render (request,"accounts/signup.html",context)

def login (request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            my_login(request,form.get_user())
            return redirect(request.GET.get("next") or "main:index")
    else:
        form = AuthenticationForm()
    context= {
        'form':form
    }
    return render (request,"accounts/login.html",context)

@login_required
def logout(request):
    my_logout(request)
    return redirect("main:index")


def detail(request,user_pk):
    pick_user= get_object_or_404(get_user_model(),pk=user_pk)
    
    context ={
        'pick_user':pick_user
    }
    return render (request,"accounts/detail.html",context)

@login_required
def update(request,user_pk):
    pick_user= get_object_or_404(get_user_model(),pk=user_pk)
    if request.user == pick_user:
        if request.method == "POST":
            form = ChangeUserInfo(request.POST ,instance=pick_user)
            if form.is_valid():
                form.save()
                return redirect ("accounts:detail",user_pk)
        else:
            form = ChangeUserInfo(instance=pick_user)
        context= {
            'form':form
        }
    return render (request,"accounts/update.html",context)

def follow (request,user_pk):
    pick_user= get_object_or_404(get_user_model(),pk=user_pk)
    if request.user == pick_user :
        pass
    elif get_user_model().followings.filter(pk=request.user).exists():
        get_user_model().followings.remove(pk=request.user)
    else:
        get_user_model().followings.add(pk=request.user)
    return redirect("accounts/detail",user_pk)

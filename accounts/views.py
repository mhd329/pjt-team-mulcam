from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .form import CreateUserForm, ChangeUserInfo, UserPhoneNumberForm
from django.contrib.auth import get_user_model, login as my_login, logout as my_logout


# Create your views here.


def signup(request):
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            my_login(request, user)
            return redirect("main:index")
    else:
        form = CreateUserForm()
    context = {
        "form": form,
    }
    return render(request, "accounts/signup.html", context)


def login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            my_login(request, form.get_user())
            return redirect(request.GET.get("next") or "main:index")
    else:
        form = AuthenticationForm()
    context = {"form": form}
    return render(request, "accounts/login.html", context)


@login_required
def logout(request):
    my_logout(request)
    return redirect("main:index")


def detail(request, user_pk):
    pick_user = get_object_or_404(get_user_model(), pk=user_pk)

    context = {"pick_user": pick_user}
    return render(request, "accounts/detail.html", context)


@login_required
def update(request, user_pk):
    pick_user = get_object_or_404(get_user_model(), pk=user_pk)
    phone = pick_user.userphonenumber
    if request.user == pick_user:
        if request.method == "POST":
            form = ChangeUserInfo(request.POST, instance=pick_user)
            pn_form = UserPhoneNumberForm(request.POST, instance=phone)
            if form.is_valid() and pn_form.is_valid():
                user = form.save()
                user_phone_number = pn_form.save(commit=False)
                user_phone_number.user = user
                phone = user_phone_number.phone
                if phone:
                    p1 = "".join(phone[:3])
                    p2 = "".join(phone[3:7])
                    p3 = "".join(phone[7:])
                    phone = "-".join([p1, p2, p3])
                    user_phone_number.phone = phone
                else:
                    pass
                user_phone_number.save()
                return redirect("accounts:detail", user_pk)
        else:
            form = ChangeUserInfo(instance=pick_user)
            pn_form = UserPhoneNumberForm(instance=phone)
        context = {
            "form": form,
            "pn_form": pn_form,
            "pick_user": pick_user,
        }
    return render(request, "accounts/update.html", context)


@login_required
def follow(request, user_pk):
    pick_user = get_object_or_404(get_user_model(), pk=user_pk)
    if request.user == pick_user:
        pass
    elif pick_user.followings.filter(pk=request.user.pk).exists():
        pick_user.followings.remove(request.user)
    else:
        pick_user.followings.add(request.user)
    return redirect("accounts:detail", user_pk)


@login_required
def delete(request, user_pk):
    pick_user = get_user_model().objects.get(pk=user_pk)
    if request.user == pick_user:
        pick_user.delete()
    return redirect("main:index")

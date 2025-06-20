from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm
from django.contrib import messages


def register(request):

    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get("username")
            messages.success(request, f"Se creó el usuario {email}")
            return redirect("landing-home")

    else:
        form = UserRegisterForm()
    title = "Registro"
    context = {"title": title, "form": form}
    return render(request, "users/register.html", context)

@login_required
def profile (request):
    return render(request, "users/profile.html")


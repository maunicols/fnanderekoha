from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import FormularioMensaje
from django.contrib.auth.models import User


def home(request):
    title = "Inicio"
    user = request.user

    initial_data = {
        "autor": user,
        "email": user.email if request.user.is_authenticated else None,
    }

    form = FormularioMensaje(
        request.POST or None,
        initial=initial_data,
        is_authenticated=user.is_authenticated,
    )
    if user.is_authenticated:
        if request.method == "POST":

            if form.is_valid():
                unchecked_form = form.save(commit=False)
                unchecked_form.autor = user
                unchecked_form.email = user.email
                unchecked_form.save()
                messages.success(request, "Gracias por tu mensaje")
                return redirect("landing-home")
    else:

        if form.is_valid():
            email = form.cleaned_data["email"]
            messages.success(request, f"Gracias por tu mensaje {email}")
            form.save()
    context = {"title": title, "form": form}

    return render(request, "landing/home.html", context)

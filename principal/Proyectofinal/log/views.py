from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from principal.models import Empleados


def index(request):
    return render(request, "log/login.html", {})


def iniciarsesion(request):
    username = request.POST['usuario']
    password = request.POST['clave']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active or user.username == 'admin':
            login(request, user)
        return HttpResponseRedirect(reverse("principal:index"))
    else:
        return render(request, "log/login.html", {})


def recuperarpassword(request):

    return render(request, "log/recuperarpassword.html", {})


def enviarcodigo(request):
    return render(request, "log/cambiarpassword.html", {})


def ingresarcodigo(request):
    return render(request, "log/ingresarcodigo.html", {})


def cambiarpassword(request):
    return HttpResponseRedirect(reverse("log:index"))


def salir(request):
    logout(request)
    return HttpResponseRedirect(reverse("log:index"))
from django.http import HttpResponseRedirect
from django.shortcuts import render
from principal.models import Domicilios
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect


def index(request):
    domicilios = Domicilios.objects.all().order_by('direccion')
    return render(request, "domicilios/domicilios.html", {'domicilios': domicilios})


def guardar(request):
    domicilio = Domicilios.objects.get(pk=request.POST['domicilio'])
    domicilio.latitud = request.POST['latitud']
    domicilio.longitud = request.POST['longitud']
    try:
        domicilio.save()
    except:
        return HttpResponseRedirect(reverse("domicilios:index"))
    return HttpResponseRedirect(reverse("domicilios:index"))

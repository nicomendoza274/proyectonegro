from django.http import HttpResponseRedirect
from django.shortcuts import render
from principal.models import Empleados
from django.db.models import Q
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect


def index(request):
    repartidores = Empleados.objects.filter(Q(tipo='Repartidor'))
    return render(request, "despacharcamion/despacharcamion.html", {'repartidores': repartidores})


def despachar(request):
    try:
        repartidor = Empleados.objects.get(id=request.POST['repdespachar'])
        estado = repartidor.enruta
        repartidor.enruta = 1 - estado
        repartidor.save()
    except:
        return HttpResponseRedirect(reverse("despacharcamion:index"))
    return HttpResponseRedirect(reverse("despacharcamion:index"))
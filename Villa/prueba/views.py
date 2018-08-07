from django.shortcuts import render
from django.db.models import Q
from principal.models import Insumos


def index(request):
    insumos = Insumos.objects.filter(Q(estado=True))
    cantidadinsumos = insumos.count()
    return render(request, "prueba/prueba.html", {'insumos':insumos, 'cantidadinsumos': cantidadinsumos})

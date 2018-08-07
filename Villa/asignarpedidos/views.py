from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from principal.models import Pedidos, Empleados, NecesidadCamion, Detalle_Pedido
from django.contrib.auth.models import User
from django.db.models import Q
from django.db import IntegrityError
import datetime
from datetime import date
# Create your views here.


def index(request):
    empleados = Empleados.objects.all()
    pedidos = Pedidos.objects.filter(Q(fecha_entrega__gte=date.today()) & Q(rep_id=0)).order_by('direccion__direccion')
    pedidosa = Pedidos.objects.filter(Q(fecha_entrega__lt=date.today()) & Q(rep_id=0)).order_by('direccion__direccion')
    return render(request, "asignarpedidos/asignarpedidos.html", {'pedidos': pedidos, 'pedidosa': pedidosa, 'empleados': empleados})


def asignar(request):
    pedido = Pedidos.objects.get(pk=request.POST['asignarempleado'])
    pedido.rep_id = Empleados.objects.get(id=request.POST['idempleado'])
    pedido.save()
    for i in pedido.detalle_pedido_set.all():
        camion, creado = NecesidadCamion.objects.get_or_create(art_id_id=i.art_id_id, emp_id_id=request.POST['idempleado'])
        if creado:
            camion.cantidad=i.cantidad
            camion.save()
        else:
            cant = camion.cantidad + i.cantidad
            camion.cantidad=cant
            camion.save()
    return HttpResponseRedirect(reverse("asignarpedidos:index"))

from django.shortcuts import render
from django.urls import reverse
from datetime import date
from principal.models import Pedidos, Empleados, Ventas, StockCamion
from django.db.models import Q
from django.http import HttpResponseRedirect
# Create your views here.


def index(request):
    dni = request.user.username
    if dni != 'admin':
        empleado = Empleados.objects.get(dni=request.user.username)
        pedidos = Pedidos.objects.filter(Q(fecha_entrega=date.today()) & Q(rep_id_id=empleado.id) & Q(estado=False)).order_by('direccion__direccion')
        stock = StockCamion.objects.filter(Q(emp_id_id=empleado.id)).order_by('art_id__nombre')
    else:
        pedidos = Pedidos.objects.filter(Q(fecha_entrega=date.today()) & Q(estado=False)).order_by('direccion__direccion')
        stock = StockCamion.objects.filter(Q(cantidad__gt=0)).order_by('art_id__nombre')
    return render(request, "verruta/verruta.html", {'pedidos': pedidos, 'stock': stock})

def registrarventa(request):
    dni = request.user.username
    if dni != 'admin':
        idpedido = request.POST['idpedido']
        pedido = Pedidos.objects.get(id=idpedido)
        pedido.estado = True
        venta = Ventas(pedido_id=idpedido, fecha=date.today(), sinpedido_id=0)
        for i in pedido.detalle_pedido_set.all():
            stock = StockCamion.objects.get(emp_id_id=pedido.rep_id_id, art_id_id=i.art_id_id)
            cant = stock.cantidad - i.cantidad
            stock.cantidad = cant
            stock.save()
        try:
            venta.save()
            pedido.save()
            return HttpResponseRedirect(reverse("verruta:index"))
        except:
            return HttpResponseRedirect(reverse("verruta:index"))
    else:
        return HttpResponseRedirect(reverse("verruta:index"))

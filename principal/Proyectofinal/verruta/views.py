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
        pedidos = Pedidos.objects.filter(Q(rep_id_id=empleado.id) & Q(estado=False)).order_by('fecha_entrega', 'direccion__direccion')
        stock = StockCamion.objects.filter(Q(emp_id_id=empleado.id)).order_by('art_id__nombre')
    else:
        pedidos = Pedidos.objects.filter(Q(estado=False)).order_by('fecha_entrega', 'direccion__direccion')
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
            try:
                stock = StockCamion.objects.get(emp_id_id=pedido.rep_id_id, art_id_id=i.art_id_id)
            except:
                dni = request.user.username
                if dni != 'admin':
                    empleado = Empleados.objects.get(dni=request.user.username)
                    pedidos = Pedidos.objects.filter(Q(rep_id_id=empleado.id) & Q(estado=False)).order_by('fecha_entrega', 'direccion__direccion')
                    stock = StockCamion.objects.filter(Q(emp_id_id=empleado.id)).order_by('art_id__nombre')
                else:
                    pedidos = Pedidos.objects.filter(Q(estado=False)).order_by('fecha_entrega', 'direccion__direccion')
                    stock = StockCamion.objects.filter(Q(cantidad__gt=0)).order_by('art_id__nombre')
                error_stockCamion = 'No hay stock disponible en el camion'
                return render(request, "verruta/verruta.html", {'pedidos': pedidos, 'stock': stock, 'error_stockCamion': error_stockCamion})
            cant = stock.cantidad - i.cantidad
            stock.cantidad = cant
            if stock.cantidad >= 0:
                try:
                    stock.save()
                    venta.save()
                    pedido.save()
                    return HttpResponseRedirect(reverse("verruta:index"))
                except:
                    return HttpResponseRedirect(reverse("verruta:index"))
            else:
                return HttpResponseRedirect(reverse("verruta:index"))
    else:
        return HttpResponseRedirect(reverse("verruta:index"))

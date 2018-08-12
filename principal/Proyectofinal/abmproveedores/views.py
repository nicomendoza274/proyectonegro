from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from principal.models import Proveedores, Insumos
from django.db.models import Q
from django.db import IntegrityError
# Create your views here.


def index(request):
    return render(request, "abmproveedores/abmproveedores.html", {'proveedores': Proveedores.objects.filter(Q(estado=True)).order_by('nombre'), 'insumos': Insumos.objects.filter(Q(estado=True))})


def buscar(request):
    proveedores = Proveedores.objects.filter(
        Q(nombre=request.POST['nombrebuscar']) | Q(telefono=request.POST['telefonobuscar']) | Q(cuit=request.POST['cuitbuscar'])
        | Q(cuentacorriente=request.POST['cuentacorrientebuscar']))
    return render(request, "abmproveedores/abmproveedores.html", {'proveedores': proveedores, })


def recargar(request):
    return HttpResponseRedirect(reverse("abmproveedores:index"))


def crearproveedor(request):
    cuit = request.POST['cuit']
    proveedor = Proveedores(nombre=request.POST['nombre'], telefono=request.POST['telefono'], cuit=cuit,
                            cuentacorriente=request.POST['cuentacorriente'], direccion=request.POST['direccion'],
                            envios=request.POST['envio'])
    buscaproveedor = Proveedores.objects.filter(Q(cuit=cuit) & Q(estado=False))
    if buscaproveedor:
        try:
            buscaproveedor.delete()
            proveedor.save()
            return HttpResponseRedirect(reverse("abmproveedores:index"))
        except IntegrityError:
            return HttpResponseRedirect(reverse("abmproveedores:index"))
    else:
        try:
            proveedor.save()
            return HttpResponseRedirect(reverse("abmproveedores:index"))
        except IntegrityError:
            return render(request, "abmproveedores/abmproveedores.html",
                          {'proveedores': Proveedores.objects.filter(Q(estado=True)),
                           'error_proveedor': 'Ya existe un proveedor con ese numero de CUIT.'})


def editarproveedor(request):
    try:
        proveedor = Proveedores.objects.get(pk=request.POST['editarproveedor'])
        proveedor.nombre=request.POST['nombre']
        proveedor.telefono=request.POST['telefono']
        proveedor.cuit = request.POST['cuit']
        proveedor.cuentacorriente=request.POST['cuentacorriente']
        proveedor.direccion=request.POST['direccion']
        proveedor.envios=request.POST['envio']
    except(KeyError):
        return HttpResponseRedirect(reverse("abmproveedores:index"))
    else:
        try:
            proveedor.save()
            return HttpResponseRedirect(reverse("abmproveedores:index"))
        except IntegrityError:
            return render(request, "abmproveedores/abmproveedores.html",
                          {'proveedores': Proveedores.objects.filter(Q(estado=True)),
                           'error_proveedor': 'Ya existe un proveedor con ese numero de CUIT.'})


def editarlistaproveedor(request):
    try:
        return HttpResponseRedirect(reverse("abmproveedores:index"))
    except:
        return HttpResponseRedirect(reverse("abmproveedores:index"))


def eliminarproveedor(request):
    try:
        proveedor = Proveedores.objects.filter(pk=request.POST['eliminarproveedor'])
        proveedor.update(estado=False)
    except(KeyError):
        return HttpResponseRedirect(reverse("abmproveedores:index"))
    else:
        for i in proveedor:
            i.save()
        return HttpResponseRedirect(reverse("abmproveedores:index"))
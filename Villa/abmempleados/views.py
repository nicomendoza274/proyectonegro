from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from principal.models import Empleados
from django.contrib.auth.models import User
from django.db.models import Q
from django.db import IntegrityError
import datetime
# Create your views here.


def index(request):
    empleados = Empleados.objects.filter(Q(estado=True)).order_by('apellido', 'nombre')
    return render(request, "abmempleados/abmempleados.html", {'empleados': empleados, })


def buscar(request):
    empleados = Empleados.objects.filter(
        Q(nombre=request.POST['nombrebuscar']) | Q(apellido=request.POST['apellidobuscar']) | Q(telefono=request.POST['telefonobuscar']) | Q(dni=request.POST['dnibuscar'])
    )
    return render(request, "abmempleados/abmempleados.html", {'empleados': empleados, })


def recargar(request):
    return HttpResponseRedirect(reverse("abmempleados:index"))


def crearempleado(request):

    dni = request.POST['dni']
    fecnac = datetime.datetime.strptime(request.POST['fecnac'], '%d/%m/%Y').strftime('%Y-%m-%d')
    empleado = Empleados(nombre=request.POST['nombre'], apellido=request.POST['apellido'], telefono=request.POST['telefono'], dni=dni, correo=request.POST['email'], direccion=request.POST['direccion'], fecNac=fecnac, tipo=request.POST['tipo'])
    buscaempleado = Empleados.objects.filter(Q(dni=dni) & Q(estado=False))
    if buscaempleado:
        try:
            user = User.objects.filter(Q(email=buscaempleado[0].correo))
            user.update(email=request.POST['email'])
            user.update(username=dni)
            user.update(password=dni)
            user.update(first_name=request.POST['tipo'])
            buscaempleado.delete()
            empleado.save()
            #enviarmailactivacion()
            return HttpResponseRedirect(reverse("abmempleados:index"))
        except IntegrityError:
            return HttpResponseRedirect(reverse("abmempleados:index"))
    else:
        try:
            empleado.save()
            User.objects.create_user(
                username=dni, password=dni, email=request.POST['email'], first_name=request.POST['tipo']
            )
            return HttpResponseRedirect(reverse("abmempleados:index"))
        except IntegrityError:
            return render(request, "abmempleados/abmempleados.html",
                          {'empleados': Empleados.objects.filter(Q(estado=True)), 'error_dni': 'Ya existe un empleado con ese dni.'})


def editarempleado(request):
    try:
        fecnac = datetime.datetime.strptime(request.POST['fecnac'], '%d/%m/%Y').strftime('%Y-%m-%d')
        empleado = Empleados.objects.get(pk=request.POST['editarempleado'])
        user = User.objects.get(username=empleado.dni)
        user.email=request.POST['email']
        user.username=request.POST['dni']
        user.first_name=request.POST['tipo']
        user.set_password(request.POST['dni'])
        empleado.nombre=request.POST['nombre']
        empleado.apellido=request.POST['apellido']
        empleado.telefono=request.POST['telefono']
        empleado.dni=request.POST['dni']
        empleado.correo=request.POST['email']
        empleado.direccion=request.POST['direccion']
        empleado.fecNac = fecnac
        empleado.tipo = request.POST['tipo']
    except(KeyError):
        return HttpResponseRedirect(reverse("abmempleados:index"))
    else:
        try:
            user.save()
            empleado.save()
            return HttpResponseRedirect(reverse("abmempleados:index"))
        except IntegrityError:
            return render(request, "abmempleados/abmempleados.html", {'empleados': Empleados.objects.filter(Q(estado=True)), 'error_dni': 'Ya existe un empleado con ese dni.'})


def eliminarempleado(request):
    try:
        empleado = Empleados.objects.filter(pk=request.POST['eliminarempleado'])
        user = User.objects.filter(Q(email=empleado[0].correo))
        user.update(is_active=False)
        empleado.update(estado=False)
    except(KeyError):
        return HttpResponseRedirect(reverse("abmempleados:index"))
    else:
        for i in empleado:
            i.save()
        return HttpResponseRedirect(reverse("abmempleados:index"))
'''
def add_enviarmailactivacion():
    return
'''
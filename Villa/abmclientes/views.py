from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from principal.models import Clientes, Domicilios
from django.db.models import Q
from django.db import IntegrityError
import datetime
# Create your views here.


def index(request):
    clientes = Clientes.objects.filter( Q(estado=True) ).order_by('apellido', 'nombre')
    return render(request, "abmclientes/abmclientes.html", {'clientes': clientes, })


def buscar(request):
    clientes = Clientes.objects.filter(
        Q(nombre=request.POST['nombrebuscar']) | Q(apellido=request.POST['apellidobuscar']) | Q(telefono=request.POST['telefonobuscar']) | Q(dni=request.POST['dnibuscar'])
    )
    return render(request, "abmclientes/abmclientes.html", {'clientes': clientes, })


def recargar(request):
    return HttpResponseRedirect(reverse("abmclientes:index"))


def crearcliente(request):
    dni = request.POST['dni']
    fecnac = datetime.datetime.strptime(request.POST['fecnac'], '%d/%m/%Y').strftime('%Y-%m-%d')
    cliente = Clientes(nombre=request.POST['nombre'], apellido=request.POST['apellido'], telefono=request.POST['telefono'], dni=dni, email=request.POST['email'], fecnac=fecnac)
    buscacliente = Clientes.objects.filter(Q(dni=dni) & Q(estado=False))
    if buscacliente:
        try:
            buscacliente.delete()
            cliente.save()
            do=Domicilios(direccion=request.POST['domicilioOriginal'], cli_id=cliente)
            do.save()
            for flag in range(len(request.POST)):
                try:
                    nd=Domicilios(direccion=request.POST['nuevo_domicilio'+str(flag)], cli_id=cliente)
                    print(nd.direccion)
                    nd.save()
                except Exception as e:
                    print(e.__cause__)
                    continue
            return HttpResponseRedirect(reverse("abmclientes:index"))
        except IntegrityError:
            return HttpResponseRedirect(reverse("abmclientes:index"))
    else:
        try:
            cliente.save()
            domicilio = Domicilios(cli_id=cliente, direccion=request.POST['domicilioOriginal'])
            domicilio.save()
            for flag in range(len(request.POST)):
                try:
                    nd=Domicilios(direccion=request.POST['nuevo_domicilio'+str(flag)], cli_id=cliente)
                    print(nd.direccion)
                    nd.save()
                except Exception as e:
                    print(e.__cause__)
                    continue
            return HttpResponseRedirect(reverse("abmclientes:index"))
        except IntegrityError as e:
            if e.__cause__ == 'UNIQUE constraint failed: principal_clientes.dni':
                error = 'DNI Existe'
            elif e.__cause__ == 'UNIQUE constraint failed: principal_clientes.email':
                error = 'Email existe'
            else:
                error = 'Hubo un error, puede que haya ingresado un dni o email ya registrado.'
            return render(request, "abmclientes/abmclientes.html", {'clientes': Clientes.objects.all(), 'error': error})


def editarcliente(request):
    try:
        fecnac=datetime.datetime.strptime(request.POST['fecnac'], '%d/%m/%Y').strftime('%Y-%m-%d')
        cliente = Clientes.objects.get(pk=request.POST['editarcliente'])
        cliente.nombre=request.POST['nombre']
        cliente.apellido=request.POST['apellido']
        cliente.telefono=request.POST['telefono']
        cliente.dni=request.POST['dni']
        cliente.email=request.POST['email']
        cliente.fecnac=fecnac
        for domicilio in cliente.domicilios_set.all():
            try:
                domicilio.direccion=request.POST[domicilio.direccion]
                domicilio.save()
            except Exception as e:
                domicilio.delete()
                continue
    except(KeyError):
        return HttpResponseRedirect(reverse("abmclientes:index"))
    else:
        try:
            cliente.save()
            for flag in range(len(request.POST)):
                try:
                    nd=Domicilios(direccion=request.POST['nuevo_domicilio'+str(flag)], cli_id=cliente)
                    nd.save()
                except:
                    continue
            return HttpResponseRedirect(reverse("abmclientes:index"))
        except IntegrityError:
            return render(request, "abmclientes/abmclientes.html", {'clientes': Clientes.objects.all(),'error':'DNI ya existe.'})


def eliminarcliente(request):
    try:
        cliente = Clientes.objects.filter(pk=request.POST['eliminarcliente'])
        cliente.update(estado=False)
    except(KeyError):
        return HttpResponseRedirect(reverse("abmclientes:index"))
    else:
        for i in cliente:
            i.save()
        return HttpResponseRedirect(reverse("abmclientes:index"))

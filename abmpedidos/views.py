import json
import datetime
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template import loader
from django.urls import reverse
from principal.models import Pedidos, Domicilios, Detalle_Pedido, Clientes, Articulos, Empleados,Contenido
from django.db.models import Q
# Create your views here.


def index(request):
    articulos_set=set()
    articulos=Articulos.objects.filter(estado=1)
    for i in articulos:
        articulos_set.add(i.nombre)
    articulos_list=list(articulos_set)
    return render(request, "abmpedidos/abmpedidos.html", {'pedidos': Pedidos.objects.filter(estado=False).order_by('fecha_entrega'), 'articulos': articulos, 'articulos_nombres': articulos_list})


def buscar(request):
    pedidos = Pedidos.objects.filter(
        Q(cli_id__dni=request.POST['dnibuscar'])
    )
    return render(request, "abmpedidos/abmpedidos.html", {'pedidos': pedidos, 'articulos': Articulos.objects.filter(estado=1)})


def recargar(request):
    return HttpResponseRedirect(reverse("abmpedidos:index"))


def crearpedido(request):
    lista_prod=[]
    lista_cant=[]
    for i in range(len(request.POST)):
        lista_cant.append(0)
    try:
        cliente=Clientes.objects.get(dni=request.POST['dni'])
        fecha_entrega=datetime.datetime.strptime(request.POST['fecha_entrega'], '%d/%m/%Y').strftime('%Y-%m-%d')
        if request.user.username != 'admin':
            EMP_PROVISORIO = Empleados.objects.get(dni=request.user.username)
        else:
            EMP_PROVISORIO = Empleados.objects.get(dni=0)
        domicilio=Domicilios.objects.get(direccion=request.POST['domicilio'])
        pedido = Pedidos(emp_id=EMP_PROVISORIO, cli_id=cliente, formapago=request.POST['forma_pago'], fecha_entrega=fecha_entrega, fecha=datetime.datetime.now(), direccion=domicilio, total=request.POST['precio_total'])
        pedido.save()
        for flag in range(len(request.POST)):
            try:
                cont = Contenido.objects.get(nom_cont=request.POST['prod_tipo'+str(flag)].split(' ')[1])
                prod = Articulos.objects.get(estado=True, nombre=request.POST['prod_nombre'+str(flag)],
                                           envase=request.POST['prod_tipo'+str(flag)].split(' ')[0],
                                           contenido = cont,
                                           capacidad=float(request.POST['prod_tipo'+str(flag)].split(' ')[2][:-1]))
                if prod not in lista_prod:
                    lista_prod.append(prod)
                lista_cant[lista_prod.index(prod)]+=int(request.POST['prod_cantidad'+str(flag)])
            except Exception as e:
                continue
        for i in range(len(lista_prod)):
            try:
                nuevo_detalle=Detalle_Pedido(ped_id=pedido, art_id=lista_prod[i], cantidad=lista_cant[i])
                nuevo_detalle.save()
            except Exception as e:
                continue
    except(KeyError):
        return render(request, "abmpedidos/abmpedidos.html", {'pedidos': Pedidos.objects.all(), 'articulos': Articulos.objects.filter(estado=1)})
    else:
        return HttpResponseRedirect(reverse("abmpedidos:index"))

def validardni(request):
    try:
        response_data = {}
        cliente = Clientes.objects.get(dni=request.GET['dni_abuscar'])
        response_data['cliente_404']=''
        response_data['cliente_nombre'] = cliente.nombre
        response_data['cliente_apellido'] = cliente.apellido
        response_data['cliente_domicilios'] = json.dumps([i.direccion for i in cliente.domicilios_set.all()])
        print(response_data['cliente_domicilios'])
        return JsonResponse(response_data)
    except:
        response_data = {}
        response_data['cliente_404']='Cliente no encontrado'
        return JsonResponse(response_data)

def modificartotal(request):
    precio=0.0
    response_data = {}
    for flag in range(len(request.GET)):
        try:
            cont = Contenido.objects.get(nom_cont=request.GET['prod_tipo'+str(flag)].split(' ')[1])
            prod = Articulos.objects.get(estado=True, nombre=request.GET['prod_nombre'+str(flag)],
                                       envase=request.GET['prod_tipo'+str(flag)].split(' ')[0],
                                       contenido = cont,
                                       capacidad=float(request.GET['prod_tipo'+str(flag)].split(' ')[2][:-1]))
            precio += prod.precio*int(request.GET['prod_cantidad'+str(flag)])
        except:
            continue
    response_data['precio']=precio
    return JsonResponse(response_data)


def buscartipos(request):
    response_data={}
    productos = Articulos.objects.filter(nombre=request.GET['producto_nombre'], estado=True)
    response_data['producto_tipos'] = json.dumps([(i.envase + ' ' + i.contenido.nom_cont + ' ' + str(i.capacidad)) for i in productos])
    return JsonResponse(response_data)

def editarpedido(request):
    try:
        pedido = Pedidos.objects.filter(pk=request.POST['editarpedido'])
        pedido.update(nombre=request.POST['nombre'], apellido=request.POST['apellido'], telefono=request.POST['telefono'], dni=request.POST['dni'], correo=request.POST['email'], direccion=request.POST['direccion'],)
    except(KeyError):
        return HttpResponseRedirect(reverse("abmpedidos:index"))
    else:
        for i in pedido:
            i.save()
        return HttpResponseRedirect(reverse("abmpedidos:index"))


def eliminarpedido(request):
    try:
        pedido = Pedidos.objects.get(pk=request.POST['eliminarpedido'])
    except(KeyError):
        return HttpResponseRedirect(reverse("abmpedidos:index"))
    else:
        pedido.delete()
        return HttpResponseRedirect(reverse("abmpedidos:index"))

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from principal.models import Insumos
from django.db.models import Q
# Create your views here.


def index(request):
    insumos = Insumos.objects.filter(estado=True).order_by('codigo')
    return render(request, "abminsumos/abminsumos.html", {'insumos': insumos,})


def buscar(request):
    nombre = request.POST['nombrebuscar'].lower()
    tipo = request.POST['tipobuscar'].lower()
    if tipo == '':
        insumos = Insumos.objects.filter(Q(nombre=nombre) & Q(estado=True))
        return render(request, "abminsumos/abminsumos.html", {'insumos': insumos,})
    elif nombre =='':
        insumos = Insumos.objects.filter(Q(tipo=tipo) & Q(estado=True))
        return render(request, "abminsumos/abminsumos.html", {'insumos': insumos,})
    elif nombre !='' and tipo != '':
        insumos = Insumos.objects.filter(Q(nombre=nombre) & Q(estado=True) & Q(tipo=tipo) )
        return render(request, "abminsumos/abminsumos.html", {'insumos': insumos,})
    else:
        return render(request, "abminsumos/abminsumos.html", {'insumos': insumos,})

def recargar(request):
    return HttpResponseRedirect(reverse("abminsumos:index"))


def crearinsumo(request):
    cap = request.POST['otro']
    tipo = request.POST['tipo']
    cod = request.POST['codinsumo']
    encod = Insumos.objects.filter(codigo=cod)
    #print(encod)
    if not encod:
        if tipo == 'contenido':
            nombre2 = request.POST['ingredientes']
            insumo = Insumos(nombre=nombre2, descripcion=request.POST['descripcion'], existenciamin=request.POST['existenciamin'], tipo=tipo, otro = 0, codigo = cod)
            buscainsumo = Insumos.objects.filter(Q(nombre=nombre2) & Q(estado=True))
            
        elif tipo == 'etiqueta':
            nombr = 'etiqueta'
            a = float(cap)
            insumo = Insumos(nombre=nombr, descripcion=request.POST['descripcion'], existenciamin=request.POST['existenciamin'], tipo=tipo, otro = a, codigo = cod)
            buscainsumo = Insumos.objects.filter(Q(nombre=nombr) & Q(otro=a) & Q(estado=True))
        else:
            nombre = request.POST['env'].lower()
            a = float(cap)
            insumo = Insumos(nombre=nombre, descripcion=request.POST['descripcion'], existenciamin=request.POST['existenciamin'], tipo=tipo, otro = a, codigo = cod)
            buscainsumo = Insumos.objects.filter(Q(nombre=nombre) & Q(otro=a) & Q(estado=True))
            
        #esta parte es para evitar repetidos  
        if buscainsumo:
            #Poner mensaje de insumo repetido
            insumos = Insumos.objects.filter(estado=True).order_by('codigo')
            error_insumoExistente = 'El insumo ya existe.'
            return render(request, "abminsumos/abminsumos.html", {'insumos': insumos, 'error_insumoExistente': error_insumoExistente})
        else:
            insumo.save()
            return HttpResponseRedirect(reverse("abminsumos:index"))
    else:
        insumos = Insumos.objects.filter(estado=True)
        error = 'Codigo existente'
        return render(request, "abminsumos/abminsumos.html", {'insumos': insumos, 'error': error})

def editarinsumo(request):
    try:
        insumo = Insumos.objects.filter(pk=request.POST['editarinsumo'])
        insumo.update(descripcion=request.POST['descripcion'], existenciamin=request.POST['existenciamin'])
    except(KeyError):
        return HttpResponseRedirect(reverse("abminsumos:index"))
    else:
        for i in insumo:
            i.save()
        return HttpResponseRedirect(reverse("abminsumos:index"))


def eliminarinsumo(request):
    try:
        insumo = Insumos.objects.filter(pk=request.POST['eliminarinsumo'])
        insumo.update(estado=False)
    except(KeyError):
        return HttpResponseRedirect(reverse("abminsumos:index"))
    else:
        for i in insumo:
            i.save()
        return HttpResponseRedirect(reverse("abminsumos:index"))

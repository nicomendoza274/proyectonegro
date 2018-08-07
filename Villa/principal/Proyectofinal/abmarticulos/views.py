from django.shortcuts import render
from principal.models import Articulos
from principal.models import Contenido
from principal.models import Insumos
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.db import IntegrityError
from principal.models import Det_Rec_Ins

def index(request):
    articulos = Articulos.objects.filter(Q(estado=True))
    cont = Contenido.objects.filter()
    ins = Insumos.objects.filter(Q(tipo='envase') & Q(estado=True))
    return render(request, "abmarticulos/abmarticulos.html", {'articulos': articulos, 'cont': cont, 'ins': ins})


def buscar(request):
    nombre = request.POST['nombrebuscar'].lower()
    envase = request.POST['envasebuscar'].lower()
    capacidad = request.POST['capacidadbuscar']
    contenido = request.POST['contenidobuscar'].lower()
    if contenido == 'agua':
        con = 1
    elif contenido == 'soda':
        con = 2
    else:
        con = 0
    if capacidad != '':
        lon = len(capacidad) - 1
        if capacidad[lon] == 'L' or capacidad[lon] == 'l':
            try:
                cap = float(capacidad.rstrip('L'))
            except:
                cap = 0
        else:
            try:
                cap = float(capacidad)
            except:
                cap = 0
    else:
        cap = 0 
    articulos = Articulos.objects.filter( ( Q(nombre=nombre) | Q(envase=envase) | Q(capacidad=cap) | Q(contenido_id=con) ) & Q(estado=True) )
    cont = Contenido.objects.filter()
    ins = Insumos.objects.filter(Q(tipo='envase') & Q(estado=True))
    return render(request, "abmarticulos/abmarticulos.html", {'articulos': articulos, 'cont':cont, 'ins': ins})


def recargar(request):
    return HttpResponseRedirect(reverse("abmarticulos:index"))

def creararticulo(request):
    nombre = request.POST['nombre'].lower()
    envase = request.POST['envase']
    articulo = Articulos(nombre=nombre, contenido_id=request.POST['contenido_id'], existenciamin=request.POST['existenciamin'],precio=request.POST['precio'])
    insumo = Insumos.objects.get(id=envase)
    buscaarticulo = Articulos.objects.filter(Q(nombre=nombre) & Q(estado=True) & Q(capacidad=insumo.otro) & Q(contenido=request.POST['contenido_id']))
    articulo.envase = insumo.nombre
    articulo.capacidad = insumo.otro
    etipiola = Insumos.objects.filter(Q(tipo = 'etiqueta') & Q(otro = insumo.otro) & Q(estado=True))
    if buscaarticulo:
        #poner aqui un mensaje "el producto existe"
        error='El producto ya existe'
        articulos = Articulos.objects.filter(Q(estado=True))
        cont = Contenido.objects.filter()
        ins = Insumos.objects.filter(Q(tipo='envase') & Q(estado=True))
        return render(request, "abmarticulos/abmarticulos.html", {'articulos': articulos, 'cont': cont, 'ins': ins, 'error_articulo': error})
    else:
        if etipiola: #si existe la etiqueta 
            if articulo.envase.lower() != 'sifon':
                articulo.save()
                if articulo.contenido_id == '1': #si es agua
                    #hacer receta de 2 insumos
                    eti = Insumos.objects.get(Q(tipo = 'etiqueta') & Q(otro = insumo.otro) & Q(estado=True))
                    receta = Det_Rec_Ins(art_id_id = articulo.id, ins_id_id = insumo.id)
                    receta.save()
                    receta2 = Det_Rec_Ins(art_id_id = articulo.id, ins_id_id = eti.id)
                    receta2.save()
                else:
                    #si no es soda entonces es un solo insumo
                    receta = Det_Rec_Ins(art_id_id = articulo.id, ins_id_id = insumo.id)
                    receta.save()
                return HttpResponseRedirect(reverse("abmarticulos:index"))
            else:
                if articulo.contenido_id == '2':
                    articulo.save()
                    receta = Det_Rec_Ins(art_id_id = articulo.id, ins_id_id = insumo.id)
                    receta.save()
                    return HttpResponseRedirect(reverse("abmarticulos:index")) 
                else:
                    #mensaje de error ("No se puede cargar un preducto Sifon con contenido Agua")   
                    articulos = Articulos.objects.filter(Q(estado=True))
                    cont = Contenido.objects.filter()
                    ins = Insumos.objects.filter(Q(tipo='envase') & Q(estado=True))
                    error_sifonAgua = 'No se puede cargar un producto Sifon con contenido Agua'
                    return render(request, "abmarticulos/abmarticulos.html", {'articulos': articulos, 'cont': cont, 'ins': ins, 'error_aguaSifon': error_sifonAgua})
        else: #si no existe la etiqueta 
            if articulo.envase == 'sifon': # si es un sifon
                if articulo.contenido_id == '2':
                    articulo.save()
                    receta = Det_Rec_Ins(art_id_id = articulo.id, ins_id_id = insumo.id)
                    receta.save()
                    return HttpResponseRedirect(reverse("abmarticulos:index")) 
                else:
                    #mensaje de error ("No se puede cargar un preducto Sifon con contenido Agua")
                    articulos = Articulos.objects.filter(Q(estado=True))
                    cont = Contenido.objects.filter()
                    ins = Insumos.objects.filter(Q(tipo='envase') & Q(estado=True))
                    error_sifonAgua = 'No se puede cargar un producto Sifon con contenido Agua'
                    return render(request, "abmarticulos/abmarticulos.html", {'articulos': articulos, 'cont': cont, 'ins': ins, 'error_aguaSifon': error_sifonAgua})
            else:
                error_etiqueta='El producto que desea crear requiere una etiqueta de la misma capacidad'
                articulos = Articulos.objects.filter(Q(estado=True))
                cont = Contenido.objects.filter()
                ins = Insumos.objects.filter(Q(tipo='envase') & Q(estado=True))
                return render(request, "abmarticulos/abmarticulos.html", {'articulos': articulos, 'cont': cont, 'ins': ins, 'error_etiqueta': error_etiqueta})



def editararticulo(request):
    try:
        articulo = Articulos.objects.get(pk=request.POST['editararticulo'])
        articulo.existenciamin=request.POST['existenciamin']
        articulo.precio = request.POST['precio']
    except(KeyError):
        return HttpResponseRedirect(reverse("abmarticulos:index"))
    else:
        try:
            articulo.save()
            return HttpResponseRedirect(reverse("abmarticulos:index"))
        except IntegrityError:
            return render(request, "abmaarticulos/abmarticulos.html", {'articulos': Articulos.objects.all(),'error_articulo':'Articulo ya existe.'})


def eliminararticulo(request):
    try:
        articulo = Articulos.objects.filter(pk=request.POST['eliminararticulo'])
        articulo.update(estado=False)
    except(KeyError):
        return HttpResponseRedirect(reverse("abmarticulos:index"))
    else:
        for i in articulo:
            i.save()
        return HttpResponseRedirect(reverse("abmarticulos:index"))

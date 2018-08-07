from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from principal.models import Detalle_Produccion
from principal.models import Copia_DetProd
from principal.models import Articulos
from principal.models import Depositos
from principal.models import Contenido
from principal.models import StockArticulos
from principal.models import StockInsumos
from django.db.models import Q
from django.db import IntegrityError
from principal.models import Det_Rec_Ins
from principal.models import Det_Contenido
from principal.models import Insumos
import datetime
# Create your views here.


def index(request):
    prod = Copia_DetProd.objects.filter(estado_reg2=True)
    art = Articulos.objects.filter(estado=True)
    dep = Depositos.objects.filter()
    cont = Contenido.objects.filter()
    return render(request, "produccion/produccion.html" , {'prod': prod, 'art': art, 'dep': dep, 'cont': cont})


def recargar(request):
    return HttpResponseRedirect(reverse("produccion:index"))

def crearcopiaprod(request):
    produccion = Copia_DetProd(cantidad2=request.POST['cantidad2'], articulo_reg2=request.POST['articulo_reg2'], deposito2=request.POST['deposito2'])
    articulo = Articulos.objects.get(id=produccion.articulo_reg2)
    produccion.capacidad2 = articulo.capacidad
    produccion.tipo_reg2 = articulo.contenido_id
    produccion.lote2 = 0 
    verifica= Copia_DetProd.objects.filter(articulo_reg2=request.POST['articulo_reg2'], deposito2=request.POST['deposito2'], capacidad2=articulo.capacidad, tipo_reg2=articulo.contenido_id)
    if verifica:
        hola = Copia_DetProd.objects.get(articulo_reg2=request.POST['articulo_reg2'], deposito2=request.POST['deposito2'], capacidad2=articulo.capacidad, tipo_reg2=articulo.contenido_id)
        cant = hola.cantidad2 + int(request.POST['cantidad2'])
        hola.cantidad2 = cant
        hola.save()
    else:
        produccion.save()
    return HttpResponseRedirect(reverse("produccion:index"))

#tablas agregadas al ultimo
def eliminartodo(request):
    try:
        produccion = Copia_DetProd.objects.all()
    except(KeyError):
        return HttpResponseRedirect(reverse("produccion:index"))
    else:
        for i in produccion:
            i.delete()
        return HttpResponseRedirect(reverse("produccion:index"))

def guardar(request):
    prod=Copia_DetProd.objects.all() #traigo toda la tabla copia del detalle de prod
    for i in prod: # recorro la tabla de copia detallle de prod
        #aqui creo el objeto prodreal con la iesima tupla de la copia (esto graba cada produccto en el historico)
        prodr = Detalle_Produccion(cantidad=i.cantidad2, articulo_reg_id=i.articulo_reg2, capacidad=i.capacidad2, tipo_reg=i.tipo_reg2, deposito=i.deposito2, lote=i.lote2)
        #aqui me filtro cada producto en el stock para saber si ya esta en el contenedor
        start = StockArticulos.objects.filter(Q(art_id_id = prodr.articulo_reg_id) & Q(dep_id_id=prodr.deposito))
        if start: #pregunto si existe el producto en el deposito
                start2=StockArticulos.objects.get(Q(art_id_id = prodr.articulo_reg_id) & Q(dep_id_id = prodr.deposito))
                #Aqui se que el objeto existe entonces traigo un sola tupla del stock
                start2.cantidad +=i.cantidad2
                #aumento el stock
                start2.save()
                #guardo 
        else: #si no existe entonces...
            #creo stock en ese dposito
            crearstart = StockArticulos(art_id_id=i.articulo_reg2, dep_id_id = i.deposito2, cantidad= i.cantidad2)
            #guardo
            crearstart.save()

        recetains = Det_Rec_Ins.objects.filter(art_id_id = prodr.articulo_reg_id) #me trae la receta del producto que estoy produciendo
        for j in recetains: #recorro el filtrado del objeto recetas de ese producto (que son los insimos que ocupa)
            band = False #seteo esta bandera para mas abajo 
            encinsum = j.ins_id_id #Guardo el id del j insumo de la receta para el producto i
            stinsumos = StockInsumos.objects.filter(ins_id_id = encinsum) #aqui filtro todos los depositos del j insumo en el stock
            for w in stinsumos: #recorro el filtrado de todos los depositos del insumo j  
                if w.cantidad >= prodr.cantidad: #reviso que el desposito tenga mas insumos de lo que quiero sacar
                    band= False # Si tengo stock suficiente la bandera se pone en flaso
                    resultado = w.cantidad - prodr.cantidad # resto lo que hay en el deposito menos el total del o que produje
                    w.cantidad = resultado #grabo la nueva cantidad
                    w.save() #por el momento salvo porque si no despues no se como salvar ??
                    break #si logro todo esto no me fijo en los otros depositos, salgo nomas
                else: #si no hay stock suficiente para sacar de un solo deposito 
                    band = True # seteo en true para despues sacar por partes 

            if band == True: #Aqui pregunto si al final del ciclio anterior no hay un deposito con el total de lo que quiero
                procan = prodr.cantidad #guardo la cantidad de lo que quiero producior 
                for w in stinsumos: #recorro el filtado de todos los depositos del insumo j
                    resultado = w.cantidad - procan #resto lo que hay en el deposito menos el total
                    if resultado < 0: # si el resultado es negativo 
                        w.cantidad= 0 #lo guardo como 0
                        w.save() #grabo 
                        procan= abs(resultado) # y lo que me queda de produccion lo hago positivo 
                    else: #en otro caso que no creo que pase por lo de arriba jajaja 
                        w.cantidad = resultado # guardo la cantidad que quedo 
                        w.save() #grabo 
        band2=False
        capacidadpiola = Articulos.objects.get(id=prodr.articulo_reg_id)
        detallecontenido = Det_Contenido.objects.all() #filtro por receta de contenidos
        encagua = Insumos.objects.get(nombre='agua mineral', otro=0, estado=True) #busco el insumo que corresponde a agua
        encdepagua = StockInsumos.objects.filter(ins_id_id=encagua.id) #aqui encuentro todos los depositos donde esta el agua
        tipoprod = prodr.tipo_reg #aqui se que tipo es (agua o soda)
        nuevacant = prodr.cantidad * capacidadpiola.capacidad 
        for w in encdepagua:
            if w.cantidad >=nuevacant:
                band2= False
                resul=w.cantidad - nuevacant
                w.cantidad = resul
                w.save()
                break
            else:
                band2 = True

        if band2 == True:
            cantreal = prodr.cantidad * capacidadpiola.capacidad
            for w in encdepagua: 
                result = encdepagua.cantidad - cantreal
                if result < 0:
                    w.cantidad = 0
                    w.save()
                    cantreal = abs(resultado)
                else:
                    w.cantidad = result
                    w.save()

        #restar gas carbonico solo cuando es soda
        if prodr.tipo_reg==2:
            band3=False
            encgas = Insumos.objects.get(nombre='gas carbónico', otro=0, estado=True) #insumo que corresponde a gascarbonico
            encdepgas = StockInsumos.objects.filter(ins_id_id=encgas.id) #aqui tengo todos los depositos donde esta el gas
            nuevacant2= prodr.cantidad * capacidadpiola.capacidad * 0.2
            for w in encdepgas:
                if w.cantidad>=nuevacant2:
                    band3 = False
                    resul2=w.cantidad - nuevacant2
                    w.cantidad = resul2
                    w.save()
                    break
                else:
                    band3 = True

            if band3 == True:
                cantreal2 = prodr.cantidad * capacidadpiola.capacidad * 0.2
                for w in encdepgas: 
                    result2 = encdepagua.cantidad - cantreal2
                    if result2 < 0:
                        w.cantidad = 0
                        w.save()
                        cantidadreal2 = abs(resultado)
                    else:
                        w.cantidad = result
                        w.save()

        prodr.save() # y a pesar de todo siempre aumenta stock :(
        
    eliminartodo('')
    return HttpResponseRedirect(reverse("produccion:index"))

#-------------------------------------------------------------------
def editarproduccion(request):
    try:
        produccion = Copia_DetProd.objects.get(id=request.POST['editarproduccion'])
        produccion.cantidad2 = request.POST['cantidad2']
        produccion.deposito2 = request.POST['deposito2']
        produccion.articulo_reg2 = request.POST['articulo_reg2']
        art = Articulos.objects.get(id = produccion.articulo_reg2)
        produccion.tipo_reg2 = art.contenido_id
        produccion.capacidad2 = art.capacidad

    except(KeyError):
        return HttpResponseRedirect(reverse("produccion:index"))
    else:
        produccion.save()
        return HttpResponseRedirect(reverse("produccion:index"))


def eliminarproduccion(request):
    try:
        produccion = Copia_DetProd.objects.filter(pk=request.POST['eliminarproduccion'])
    except(KeyError):
        return HttpResponseRedirect(reverse("produccion:index"))
    else:
        for i in produccion:
            i.delete()
        return HttpResponseRedirect(reverse("produccion:index"))


#aqui empieza lo de fer
def index2(request):
    prod = Detalle_Produccion.objects.all().order_by('-fecha_reg')
    art = Articulos.objects.filter(estado=True)
    cont = Contenido.objects.filter()
    dep = Depositos.objects.all()
    return render(request, "produccion/consultaproduccion.html" , {'prod': prod, 'art': art, 'cont':cont, 'dep':dep})

def recargar2(request):
    return HttpResponseRedirect(reverse("produccion:index2"))

def buscar(request):
    try:
        if request.POST['buscarpor']=="0":
            try:

                    if request.POST['fecdesde'] and request.POST['fechasta']:   
                        fecd=datetime.datetime.strptime(request.POST['fecdesde'],'%d/%m/%Y').strftime('%Y-%m-%d')
                        fech=datetime.datetime.strptime(request.POST['fechasta'],'%d/%m/%Y').strftime('%Y-%m-%d')
                        cont = Contenido.objects.all()
                        dep = Depositos.objects.all()
                        art = Articulos.objects.filter(estado=True)
                        if request.POST['numdep']!="0":
                            prod = Detalle_Produccion.objects.filter(Q(fecha_reg__range=(fecd,fech)) & Q(deposito=request.POST['numdep'])).order_by('-fecha_reg')
                        else:
                            prod = Detalle_Produccion.objects.filter(Q(fecha_reg__range=(fecd,fech))).order_by('-fecha_reg')
                        return render(request, "produccion/consultaproduccion.html" , {'prod': prod, 'art': art, 'cont':cont, 'dep':dep})

                    else:
                        cont = Contenido.objects.all()
                        dep = Depositos.objects.all()
                        art = Articulos.objects.filter(estado=True)
                        if request.POST['numdep']!="0":
                            prod = Detalle_Produccion.objects.filter(Q(deposito=request.POST['numdep'])).order_by('-fecha_reg')
                        else:
                            prod = Detalle_Produccion.objects.filter().order_by('-fecha_reg')
                        return render(request, "produccion/consultaproduccion.html" , {'prod': prod, 'art': art, 'cont':cont, 'dep':dep})
            except IntegrityError:
                return HttpResponseRedirect(reverse("produccion:index2"))
        elif request.POST['buscarpor']=="1":
            try:
                    if request.POST['fecdesde'] and request.POST['fechasta']:          
                        fecd=datetime.datetime.strptime(request.POST['fecdesde'],'%d/%m/%Y').strftime('%Y-%m-%d')
                        fech=datetime.datetime.strptime(request.POST['fechasta'],'%d/%m/%Y').strftime('%Y-%m-%d')
                        cont = Contenido.objects.filter(nom_cont=request.POST['busqueda'])
                        art = Articulos.objects.filter(estado=True)
                        dep = Depositos.objects.all()
                        if request.POST['numdep']!="0":
                            prod = Detalle_Produccion.objects.filter(Q(tipo_reg=cont) & Q(fecha_reg__range=(fecd,fech)) & Q(deposito=request.POST['numdep'])).order_by('-fecha_reg')
                        else:
                            prod = Detalle_Produccion.objects.filter(Q(tipo_reg=cont) & Q(fecha_reg__range=(fecd,fech))).order_by('-fecha_reg')
                        return render(request, "produccion/consultaproduccion.html" , {'prod': prod, 'art': art, 'cont':cont, 'dep':dep})
                    else:
                        cont = Contenido.objects.filter(nom_cont=request.POST['busqueda'])
                        dep = Depositos.objects.all()
                        art = Articulos.objects.filter(estado=True)
                        if request.POST['numdep']!="0":
                            prod = Detalle_Produccion.objects.filter(Q(tipo_reg=cont) & Q(deposito=request.POST['numdep'])).order_by('-fecha_reg')
                        else:
                            prod = Detalle_Produccion.objects.filter(Q(tipo_reg=cont)).order_by('-fecha_reg')
                        return render(request, "produccion/consultaproduccion.html" , {'prod': prod, 'art': art, 'cont':cont, 'dep':dep})
            except IntegrityError:
                return HttpResponseRedirect(reverse("produccion:index2"))
        elif request.POST['buscarpor']=="2": 
            try:
                    if request.POST['fecdesde'] and request.POST['fechasta']: 
                        fecd=datetime.datetime.strptime(request.POST['fecdesde'],'%d/%m/%Y').strftime('%Y-%m-%d')
                        fech=datetime.datetime.strptime(request.POST['fechasta'],'%d/%m/%Y').strftime('%Y-%m-%d')
                        cont = Contenido.objects.all()
                        dep = Depositos.objects.all()
                        art = Articulos.objects.filter(Q(estado=True) & Q(nombre=request.POST['busqueda']))
                        
                        
                        if request.POST['numdep']!="0":
                            prod = Detalle_Produccion.objects.filter(Q(articulo_reg=art) & Q(fecha_reg__range=(fecd,fech)) & Q(deposito=request.POST['numdep'])).order_by('-fecha_reg')
                        else:
                            prod = Detalle_Produccion.objects.filter(Q(articulo_reg=art) & Q(fecha_reg__range=(fecd,fech))).order_by('-fecha_reg')
                        return render(request, "produccion/consultaproduccion.html" , {'prod': prod, 'art': art, 'cont':cont, 'dep':dep})
                    else:
                        cont = Contenido.objects.all()
                        dep = Depositos.objects.all()
                        art = Articulos.objects.filter(Q(estado=True) & Q(nombre=request.POST['busqueda']))
                        
                        if request.POST['numdep']!="0":
                            prod = Detalle_Produccion.objects.filter(Q(articulo_reg=art) & Q(deposito=request.POST['numdep'])).order_by('-fecha_reg')
                        else:
                            prod = Detalle_Produccion.objects.filter(Q(articulo_reg=art)).order_by('-fecha_reg')               
                        return render(request, "produccion/consultaproduccion.html" , {'prod': prod, 'art': art, 'cont':cont, 'dep':dep})
            except IntegrityError:
                return HttpResponseRedirect(reverse("produccion:index2")) 
    except IntegrityError:
            return HttpResponseRedirect(reverse("produccion:index2"))


from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from principal.models import Detalle_Produccion
from principal.models import Copia_DetProd, Copia_Remitos
from principal.models import Articulos
from principal.models import Insumos
from principal.models import Depositos
from principal.models import Contenido
from principal.models import StockArticulos
from principal.models import StockInsumos
from django.db.models import Q
from django.db import IntegrityError
from principal.models import Det_Rec_Ins
from principal.models import Det_Contenido
from principal.models import Proveedores
from principal.models import Copia_DetRem
from principal.models import Remitos
from principal.models import Detalle_Remito
import datetime
from django.http import JsonResponse
# Create your views here.

def recargar(request):
    return HttpResponseRedirect(reverse("remito:index"))

def recargar2(request):
    return HttpResponseRedirect(reverse("remito:index2"))

def index3(request):
    art = Articulos.objects.filter(estado=True)
    dep = Depositos.objects.all()
    det = Copia_DetRem.objects.all()
    cont = Contenido.objects.filter()
    ins = Insumos.objects.all()
    prov = Proveedores.objects.filter(estado=True)
    rem = Remitos.objects.all()
    return render(request, "remito/cabecera.html" , {'det': det, 'ins': ins, 'dep': dep, 'rem': rem, 'cont': cont, 'prov': prov})

def index2(request):
    art = Articulos.objects.filter(estado=True)
    dep = Depositos.objects.all()
    det = Copia_DetRem.objects.all()
    cont = Contenido.objects.filter()
    ins = Insumos.objects.all()
    prov = Proveedores.objects.filter(estado=True)
    rem = Remitos.objects.all()
    cab = Copia_Remitos.objects.all()[0]

    return render(request, "remito/nuevoremito.html" , {'det': det, 'ins': ins, 'dep': dep, 'cab': cab, 'rem': rem, 'cont': cont, 'prov': prov})

def index(request): #consultarremito
    dep = Depositos.objects.all()
    det = Copia_DetRem.objects.all()
    cont = Contenido.objects.filter()
    ins = Insumos.objects.all()
    #art = Articulos.objects.filter()
    prov = Proveedores.objects.filter()
    rem = Remitos.objects.all().order_by('codigo')
    return render(request, "remito/consultarremito.html" , {'det': det, 'ins': ins, 'dep': dep, 'rem': rem, 'cont': cont,'prov': prov})

def validarremito(request):
    try:
        response_data = {}
        insumo = Insumos.objects.get(codigo=request.GET['codigo_abuscar'])
        print(insumo.nombre)
        response_data['insumo_404']=''
        response_data['insumo_nombre'] = insumo.nombre
        response_data['insumo_descripcion'] = insumo.descripcion
        return JsonResponse(response_data)
    except:
        response_data = {}
        response_data['insumo_404']='Insumo no encontrado'
        return JsonResponse(response_data)

def crearcopiaremito(request):
    try:
        depo = Depositos.objects.get(pk=request.POST['numdep'])
        insumo = Insumos.objects.get(codigo=request.POST['codigo'])
        fechaven=datetime.datetime.strptime(request.POST['fecven'],'%d/%m/%Y').strftime('%Y-%m-%d')
        detremito = Copia_DetRem(cant_recib2=request.POST['cantidad2'], ins_id2=insumo, vencimiento2= fechaven, codigo2=request.POST['codigo'], rem_id2 = 1, dep_id2=depo)    

    except(KeyError):
        return render(request, "remito/nuevoremito.html", {'remito': Copia_DetRem.objects.all(),})
    else:
        detremito.save()
        return HttpResponseRedirect(reverse("remito:index2"))


def eliminartodo(request):
    try:
        detremito = Copia_DetRem.objects.all()
        rem=Copia_Remitos.objects.all()
    except(KeyError):
        return HttpResponseRedirect(reverse("remito:index"))
    else:
        for a in rem:
            a.delete()
        for i in detremito:
            i.delete()
        return HttpResponseRedirect(reverse("remito:index"))

def guardar(request):
    rem=Copia_DetRem.objects.all()
    copiacab = Copia_Remitos.objects.all()[0]
    #fecremito=datetime.datetime.strptime(copiacab.fecha_recib2,'%d/%m/%Y').strftime('%Y-%m-%d')
    prove=Proveedores.objects.get(pk=copiacab.prov_id2_id)
    cabezaremito = Remitos(prov_id = prove, fecha_recib = copiacab.fecha_recib2, codigo = copiacab.codigo2)
    cabezaremito.save()

    for i in rem:
        try:
            dep = Depositos.objects.get(pk=i.dep_id2_id)
            insumo2=Insumos.objects.get(pk=i.ins_id2_id)
            codremito = Remitos.objects.get(codigo=copiacab.codigo2)
            detremito = Detalle_Remito(cant_recib=i.cant_recib2, ins_id=insumo2, dep_id=dep, vencimiento=i.vencimiento2, rem_id=codremito)
            stins = StockInsumos.objects.filter(Q(ins_id= i.ins_id2) & Q(dep_id=dep))
            #cantidad = models.IntegerField()
            if stins:
                    stins2=StockInsumos.objects.get(Q(ins_id = i.ins_id2) & Q(dep_id = dep))
                    stins2.cantidad +=i.cant_recib2
                    stins2.save()
            else:
                ins=Insumos.objects.get(pk=i.ins_id2_id)
                cantidad= i.cant_recib2
                crearstins = StockInsumos(ins_id=ins, dep_id = dep, cantidad= cantidad)
                crearstins.save()
        except(KeyError):
            return render(request, "remito/nuevoremito.html")
        else:
            detremito.save() # y a pesar de todo siempre aumenta stock :(
    eliminartodo('')
    return HttpResponseRedirect(reverse("remito:index"))

def editardetalle(request):
    try:
        fecremit=datetime.datetime.strptime(request.POST['fecrem'],'%d/%m/%Y').strftime('%Y-%m-%d')
        prov=Proveedores.objects.get(prov_id2=request.POST['nomprov'])
        cabecera = Copia_Remitos.objects.get(Q(codigo2=request.POST['codigo']) & Q(prov_id2=request.POST['nomprov']))
        cabecera.prov_id2= prov
        cabecera.fecha_recib2= fectemit
        cabecera.codigo2 = request.POST['codigo']

    except(KeyError):
        return HttpResponseRedirect(reverse("remito:index2"))
    else:
        cabecera.save()
        return HttpResponseRedirect(reverse("remito:index2"))

def editarcabecera(request):
    try:
        fecven=datetime.datetime.strptime(request.POST['fecven'],'%d/%m/%Y').strftime('%Y-%m-%d')
        cabecera = Copia_DetRem.objects.get(id=request.POST['editardetalle'])
        detalle.cant_recib2 = request.POST['canti']
        detalle.vencimiento2 = fecven

    except(KeyError):
        return HttpResponseRedirect(reverse("remito:index2"))
    else:
        detalle.save()
        return HttpResponseRedirect(reverse("remito:index2"))

def eliminardetalle(request):
    try:
        detalle = Copia_DetRem.objects.filter(pk=request.POST['eliminardetalle'])
    except(KeyError):
        return HttpResponseRedirect(reverse("remito:index2"))
    else:
        for i in detalle:
            i.delete()
        return HttpResponseRedirect(reverse("remito:index2"))

def cabecera(request):
    #cab=Copia_Remitos.objects.all()
    #hola=int(request.POST['nombprov'])
    #prov = Proveedores.objects.get(pk=hola)
   # dep = Depositos.objects.get(pk=request.POST['numdep'])

    if request.POST['nombprov'] and request.POST['codrem'] and request.POST['fecrem']:
        fecremito=datetime.datetime.strptime(request.POST['fecrem'],'%d/%m/%Y').strftime('%Y-%m-%d')
        pro = Proveedores.objects.get(pk=request.POST['nombprov'])
        cabezaremito = Copia_Remitos(prov_id2 = pro, fecha_recib2 = fecremito, codigo2 = request.POST['codrem'])
        cabezaremito.save()
        return HttpResponseRedirect(reverse("remito:index2"))
    else:
        return HttpResponseRedirect(reverse("remito:index3"))

def buscar(request):
    dep = Depositos.objects.all()
    det = Copia_DetRem.objects.all()
    cont = Contenido.objects.filter()
    ins = Insumos.objects.all()
    prov = Proveedores.objects.filter(estado=True)
    rem = Remitos.objects.all().order_by('codigo')

    idprov=request.POST['buscarpor']
    

    if idprov == 0: 
        #todos los proveedores
        if request.POST['fecdesde'] and request.POST['fechasta']:
            #limita con fechas   
            fecd=datetime.datetime.strptime(request.POST['fecdesde'],'%d/%m/%Y').strftime('%Y-%m-%d')
            fech=datetime.datetime.strptime(request.POST['fechasta'],'%d/%m/%Y').strftime('%Y-%m-%d')
            rem = Remitos.objects.filter( Q (fecha_recib__range=(fecd,fech) ) )#.order_by('-fecha_reg')
            return render(request, "remito/consultarremito.html" , {'det': det, 'ins': ins, 'dep': dep, 'rem': rem, 'cont': cont,'prov': prov})
        else:
            return render(request, "remito/consultarremito.html" , {'det': det, 'ins': ins, 'dep': dep, 'rem': rem, 'cont': cont,'prov': prov})
    else:
        return render(request, "remito/consultarremito.html" , {'det': det, 'ins': ins, 'dep': dep, 'rem': rem, 'cont': cont,'prov': prov})
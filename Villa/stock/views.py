#para el reporte
import os
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from django.views.generic import ListView
from reportlab.platypus import SimpleDocTemplate, Paragraph, TableStyle, PageBreak, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Table, LongTable
from reportlab.lib.enums import TA_CENTER
#finreporte
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from principal.models import Insumos, Depositos
from principal.models import StockInsumos
from django.db.models import Q
from datetime import datetime
from datetime import date
# Create your views here.



def index(request):
    stockinsumos = StockInsumos.objects.filter().order_by('dep_id_id')
    insumos = Insumos.objects.filter()
    dep = Depositos.objects.filter()
    return render(request, "stock/stock.html" , {'stockinsumos': stockinsumos, 'insumos': insumos, 'dep': dep})

def buscar(request):
    depnum = request.POST['numdepo']
    nombre2=request.POST['nombrebuscar']
    dep = Depositos.objects.filter()
    if depnum!='0':
        #elige algun num de deposito
        if nombre2 != '':
            #cuando pone nombre y elige depo
            try:
                insumos = Insumos.objects.filter(Q(nombre__istartswith=nombre2) ).order_by('nombre')
                stockinsumos = StockInsumos.objects.filter(Q(ins_id = insumos) & Q(dep_id_id = depnum))
                return render(request, "stock/stock.html", {'stockinsumos': stockinsumos, 'insumos': insumos, 'dep': dep})
            except(KeyError):
                return render(request, "stock/stock.html", {'stockinsumos': stockinsumos, 'insumos': insumos, 'dep': dep})
        else:
            #cuando solo pone depo
            try:
                insumos = Insumos.objects.filter()
                stockinsumos = StockInsumos.objects.filter(Q(dep_id_id = depnum) ) 
                return render(request, "stock/stock.html", {'stockinsumos': stockinsumos, 'insumos': insumos, 'dep': dep})
            except(KeyError):
                return render(request, "stock/stock.html", {'stockinsumos': stockinsumos, 'insumos': insumos, 'dep': dep})
    #elige todos los depo
    else:
        if nombre2 == '':
            #todos los depo sin nombre de busqueda
            return HttpResponseRedirect(reverse("stock:index"))
        else:
            #todos los depo con nombre de busqueda
            try:
                insumos = Insumos.objects.filter(Q(nombre__istartswith=nombre2 ) )
                stockinsumos = StockInsumos.objects.filter(Q(ins_id = insumos) ).order_by('dep_id_id')
                return render(request, "stock/stock.html", {'stockinsumos': stockinsumos, 'insumos': insumos, 'dep': dep})
            except(KeyError):
                return render(request, "stock/stock.html", {'stockinsumos': stockinsumos, 'insumos': insumos, 'dep': dep})


def recargar(request):
    return HttpResponseRedirect(reverse("stock:index")) 

def report (request):
    response = HttpResponse (content_type='application/pdf')
    insumos = Insumos.objects.all()
    stockinsumos = StockInsumos.objects.all()

    #nombre pdf

    d = datetime.now()
    '/'.join(str(x) for x in (d.month, d.day, d.year))
    d2= date.today()

    name = "reporte-insumos-" + str (d) + ".pdf"
    response['Content-Disposition'] = 'attachment; filename=%s' % name
 

    #creo el pdf
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)

    #encabezado
    c.setLineWidth(.3)
    c.setFont('Helvetica', 22)
    c.drawString (30, 750, 'Villa del Norte')
    
    c.setFont('Helvetica', 12)
    c.drawString (30, 735, 'Informe de insumos con bajas existencias')

    c.setFont('Helvetica-Bold', 12)
    c.drawString (480, 750, str (d2))
    c.line(460,747,560,747)

    #table header
    styles = getSampleStyleSheet ()
    styleBH = styles["Normal"]
    styleBH.alignment=TA_CENTER
    styleBH.fontSize = 10

    nom = Paragraph ('''NOMBRE''', styleBH)
    numdep= Paragraph ('''DEPOSITO''', styleBH)
    exmin = Paragraph ('''EXISTENCIA MINIMA''', styleBH)
    exact = Paragraph ('''EXISTENCIA ACTUAL''', styleBH)
    falt = Paragraph ('''FALTANTE''', styleBH)

    data = []

    data.append ([nom, numdep, exmin, exact, falt])

    #table
    styleN = styles["BodyText"]
    styleN.alignment=TA_CENTER
    styleN.fontSize = 9

    high = 700

    band= False

    for ins in insumos:
        for st in stockinsumos:
            if st.ins_id_id  == ins.id:
                if st.cantidad < ins.existenciamin:
                    band= True
                    act = st.cantidad
                    minim = ins.existenciamin
                    faltante = minim - act
                    deposito = Depositos.objects.get(id=st.dep_id_id)
                    nom = Paragraph (str (ins.nombre).title(), styleN)
                    numdep= Paragraph (str (deposito.ubicacion), styleN)
                    exmin = Paragraph ( str (ins.existenciamin), styleN)
                    exact = Paragraph ( str (st.cantidad), styleN)
                    falt = Paragraph ( str (faltante), styleN)
                    this_ins = [ nom, numdep, exmin, exact, falt ]
                    data.append(this_ins)
                    high = high - 18


    if band == True:
        #table size
        width, height = A4
        table = Table (data, colWidths=[2.5 * cm, 3.2 * cm, 4 * cm, 4.5 * cm, 3 * cm], repeatRows=1)
        table.setStyle (TableStyle ([ # estilos de la tabla
            ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
            ('BOX', (0, 0), (-1, -1), 0.25, colors.black), ]))
        
        #pdf size
        table.wrapOn(c, width, height)
        table.drawOn(c, 30, high)
        c.showPage () #save page

        #save pdf
        c.save()
        #get te value of BytesIO buffer and write response
        pdf = buffer.getvalue()
        buffer.close()
        response.write (pdf)
    else:
        data = []
        c.setFont('Helvetica', 9)
        c.drawString (30, 690, 'No se registraron bajas existencias de insumos en el día de la fecha')
        
        c.showPage () #save page

        #save pdf
        c.save()
        #get te value of BytesIO buffer and write response
        pdf = buffer.getvalue()
        buffer.close()
        response.write (pdf)
    return response
#para el reporte
import os
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, cm
from django.views.generic import ListView
from reportlab.platypus import SimpleDocTemplate, Paragraph, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Table
from reportlab.lib.enums import TA_CENTER
#finreporte
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from principal.models import Articulos, Depositos
from django.db.models import Q
from principal.models import StockArticulos
from datetime import datetime
from datetime import date
# Create your views here.

def index(request):
    articulos = Articulos.objects.filter()
    stockarticulos = StockArticulos.objects.filter().order_by('dep_id_id')
    dep = Depositos.objects.filter()
    return render(request, "stockart/stockart.html" , {'stockarticulos': stockarticulos, 'articulos': articulos, 'dep': dep})


def busart(request):
	depnum = request.POST['numdepo']
	nombre2 = request.POST['nombrebuscar']
	dep = Depositos.objects.filter()
	if depnum!='0':
		#elige algun num de deposito
		if nombre2 != '':
            #cuando pone nombre y elige depo
			try:
				articulos = Articulos.objects.filter(Q(nombre__istartswith=nombre2 ) ).order_by('nombre')
				stockarticulos = StockArticulos.objects.filter(Q(art_id_id = articulos) & Q(dep_id_id = depnum))
				return render(request, "stockart/stockart.html", {'stockarticulos': stockarticulos, 'articulos': articulos, 'dep': dep})
			except(KeyError):
				return render(request, "stockart/stockart.html", {'stockarticulos': stockarticulos, 'articulos': articulos, 'dep': dep})
		else:
			try:
				#cuando solo pone depo
				stockarticulos = StockArticulos.objects.filter(Q(dep_id_id = depnum)) 
				articulos = Articulos.objects.filter().order_by('nombre')            
				return render(request, "stockart/stockart.html", {'stockarticulos':stockarticulos, 'articulos': articulos, 'dep': dep})
			except(KeyError):
				return render(request, "stockart/stockart.html", {'stockarticulos': stockarticulos, 'articulos': articulos, 'dep': dep})
    #elige todos los depo
	else:
		if nombre2 == '':
            #todos los depo sin nombre de busqueda
			return HttpResponseRedirect(reverse("stockart:index"))
		else: 
			#todos los depo con nombre de busqueda
			try:
				articulos = Articulos.objects.filter(Q(nombre__istartswith=nombre2 ) )
				stockarticulos = StockArticulos.objects.filter(Q(art_id = articulos)).order_by('dep_id_id')
				return render(request, "stockart/stockart.html", {'stockarticulos': stockarticulos, 'articulos': articulos, 'dep': dep})
			except(KeyError):
				return render(request, "stockart/stockart.html", {'stockarticulos': stockarticulos, 'articulos': articulos, 'dep': dep})


def recargar(request):
    return HttpResponseRedirect(reverse("stockart:index"))

def report (request):
    response = HttpResponse (content_type='application/pdf')
    articulos = Articulos.objects.all()
    stockarticulos = StockArticulos.objects.all()

    #nombre pdf

    d = datetime.now()
    '/'.join(str(x) for x in (d.month, d.day, d.year))
    d2= date.today()

    name = "reporte-productos-" + str (d) + ".pdf"
    response['Content-Disposition'] = 'attachment; filename=%s' % name
 

    #creo el pdf
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)

    #encabezado
    c.setLineWidth(.3)
    c.setFont('Helvetica', 22)
    c.drawString (30, 750, 'Villa del Norte')
    
    c.setFont('Helvetica', 12)
    c.drawString (30, 735, 'Informe de productos con bajas existencias')

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
    styleN.fontSize = 8

    high = 700

    band= False

    for art in articulos:
        for st in stockarticulos:
            if st.art_id_id  == art.id:
                if st.cantidad < art.existenciamin:
                    band= True
                    act = st.cantidad
                    minim = art.existenciamin
                    faltante = minim - act
                    deposito = Depositos.objects.get(id=st.dep_id_id)
                    nom = Paragraph (str (art.nombre).title(), styleN)
                    numdep= Paragraph (str (deposito.ubicacion), styleN)
                    exmin = Paragraph ( str (art.existenciamin), styleN)
                    exact = Paragraph ( str (st.cantidad), styleN)
                    falt = Paragraph ( str (faltante), styleN)
                    this_art = [ nom, numdep, exmin, exact, falt ]
                    data.append(this_art)
                    high = high - 18
        

    if band == True:
        #table size
        width, height = A4
        table = Table (data, colWidths=[2.5 * cm, 3.2 * cm, 4 * cm, 4.5 * cm, 3 * cm])
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
        c.drawString (30, 690, 'No se registraron bajas existencias de productos en el día de la fecha')
        
        c.showPage () #save page

        #save pdf
        c.save()
        #get te value of BytesIO buffer and write response
        pdf = buffer.getvalue()
        buffer.close()
        response.write (pdf)

    return response

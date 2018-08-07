from django.shortcuts import render
from django.urls import reverse
from datetime import date
from principal.models import StockArticulos, StockCamion, NecesidadCamion, Depositos
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from datetime import datetime
from datetime import date
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
# Create your views here.


def index(request):
    camiones = StockCamion.objects.filter(Q(cantidad__gt=0) & Q(emp_id__enruta=0)).order_by('emp_id', )
    depositos = Depositos.objects.all()
    return render(request, "descargarcamion/descargarcamion.html", {'camiones': camiones, 'depositos': depositos})


def descargar(request):
    errores = ''
    if request.method == "POST":
        values = request.POST.getlist('inpu')
        for i in values:
            print(i)
            datos = i.split('-')
            emp = datos[0]
            art = datos[1]
            cant = int(datos[2])
            dep = Depositos.objects.get(ubicacion=datos[3])
            #try:
            camion = StockCamion.objects.get(emp_id=emp, art_id=art)
            stocksuficiente = camion.cantidad - cant
            #if (stocksuficiente >= 0):
            articulostock, creado = StockArticulos.objects.get_or_create(dep_id_id=dep.id, art_id_id=art)
            if creado:
                articulostock.cantidad = cant
            else:
                articulostock.cantidad += cant
            necesidad, ncreado = NecesidadCamion.objects.get_or_create(emp_id_id=emp, art_id_id=art)
            if ncreado:
                necesidad.cantidad = cant
            else:
                necesidad.cantidad += cant
            #try:
            necesidad.save()
            articulostock.save()
            camion.delete()
            #except Exception as e:
                # print(e)
             #   continue
            #else:
                    #errores = errores+art
            #except:
             #   continue
                #errores = errores+art
    #largo = len(errores)
    #return render(request, "cargarcamion/cargarcamion.html",
    #              {'empleados': empleados, 'depositos': depositos, 'errores': errores, 'largo': largo})
    return HttpResponseRedirect(reverse("descargarcamion:index"))


def report(request):
    response = HttpResponse(content_type='application/pdf')
    carga = NecesidadCamion.objects.filter(Q(cantidad__gt=0)).order_by('emp_id_id')

    # nombre pdf

    d = datetime.now()
    '/'.join(str(x) for x in (d.month, d.day, d.year))
    d2 = date.today()

    name = "productosACargar-" + str(d) + ".pdf"
    response['Content-Disposition'] = 'attachment; filename=%s' % name

    # creo el pdf
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)

    # encabezado
    c.setLineWidth(.3)
    c.setFont('Helvetica', 22)
    c.drawString(30, 750, 'Villa del Norte')

    c.setFont('Helvetica', 12)
    c.drawString(30, 735, 'Productos a cargar')

    c.setFont('Helvetica-Bold', 12)
    c.drawString(480, 750, str(d2))
    c.line(460, 747, 560, 747)

    # table header
    styles = getSampleStyleSheet()
    styleBH = styles["Normal"]
    styleBH.alignment = TA_CENTER
    styleBH.fontSize = 10

    nombre = Paragraph('''NOMBRE''', styleBH)
    dni = Paragraph('''DNI''', styleBH)
    producto = Paragraph('''PRODUCTO''', styleBH)
    cantidad = Paragraph('''CANTIDAD''', styleBH)
    deposito = Paragraph('''DEPOSITO''', styleBH)

    data = []

    data.append([nombre, dni, producto, cantidad, deposito])

    # table
    styleN = styles["BodyText"]
    styleN.alignment = TA_CENTER
    styleN.fontSize = 9

    high = 700

    for car in carga:
        nombre = Paragraph(str(car.emp_id.nombre), styleN)
        dni = Paragraph(str(car.emp_id.dni), styleN)
        capacidad= str(car.art_id.capacidad)
        producto = Paragraph(str(car.art_id.nombre+' '+car.art_id.envase+' '+capacidad), styleN)
        cantidad = Paragraph(str(car.cantidad), styleN)
        deposito = Paragraph(str(' '), styleN)
        this_ins = [nombre, dni, producto, cantidad,deposito]
        data.append(this_ins)
        high = high - 18

    # table size
    width, height = A4
    table = Table(data, colWidths=[2.5 * cm, 3.2 * cm, 4 * cm, 4.5 * cm, 3 * cm], repeatRows=1)
    table.setStyle(TableStyle([  # estilos de la tabla
        ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
        ('BOX', (0, 0), (-1, -1), 0.25, colors.black), ]))

    # pdf size
    table.wrapOn(c, width, height)
    table.drawOn(c, 30, high)
    c.showPage()  # save page

    # save pdf
    c.save()
    # get te value of BytesIO buffer and write response
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response

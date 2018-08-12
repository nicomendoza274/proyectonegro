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
from reportlab.lib.pagesizes import A4, cm
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
    #e.id, e.nombre, e.apellido, a.nombre, a.capacidad, a.envase, sum(d.cantidad)
    #mapa = {'e_id': 'e.id', 'e_nombre': 'e.nombre', 'e_apellido': 'e.apellido', 'a_nombre': 'a.nombre', 'a_capacidad': 'a.capacidad', 'a_envase': 'a.envase', 'cantidad': 'sum(d.cantidad)'}
    #empleados = list(Detalle_Pedido.objects.raw('''select *,sum(d.cantidad) as suma from principal_detalle_pedido d
    #                                  join principal_articulos a on a.id=d.art_id_id
    #                                  join principal_pedidos p on d.ped_id_id=p.id
    #                                  join principal_empleados e on e.id=p.rep_id_id
    #                                  where (p.fecha_entrega=date(\'now\',\'-3 hour\') and p.estado=0)
    #                                 group by e.id,a.id;'''))
    empleados = NecesidadCamion.objects.filter(Q(cantidad__gt=0)).order_by('emp_id_id')
    depositos = Depositos.objects.all()
    return render(request, "cargarcamion/cargarcamion.html", {'empleados': empleados, 'depositos': depositos})


def cargar(request):
    #Falta modificar el stock desde algun deposito
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
            try:
                deposito = StockArticulos.objects.get(dep_id=dep.id, art_id=art)
                stocksuficiente = deposito.cantidad - cant
                if (stocksuficiente >= 0):
                    detalle, creado = StockCamion.objects.get_or_create(emp_id_id=emp, art_id_id=art)
                    detalle.cantidad = cant
                    necesidad = NecesidadCamion.objects.get(art_id_id=art, emp_id_id=emp)
                    deposito.cantidad = stocksuficiente
                    try:
                        detalle.save()
                        necesidad.delete()
                        deposito.save()
                    except Exception as e:
                        # print(e)
                        continue
                #else:
                    #errores = errores+art
            except:
                continue
                #errores = errores+art
    #largo = len(errores)
    #return render(request, "cargarcamion/cargarcamion.html",
    #              {'empleados': empleados, 'depositos': depositos, 'errores': errores, 'largo': largo})
    return HttpResponseRedirect(reverse("cargarcamion:index"))


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

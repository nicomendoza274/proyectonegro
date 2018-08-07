from django.db import models
from datetime import date


# Create your models here.
class Empleados(models.Model):
    nombre = models.CharField(max_length=30)
    apellido = models.CharField(max_length=30)
    correo = models.CharField(max_length=30)
    fecIng = models.DateField(default=date.today)
    fecNac = models.DateField(default=date.today)
    tipo = models.CharField(max_length=20)
    dni = models.CharField(max_length=8, unique=True)
    telefono = models.CharField(max_length=13)
    direccion = models.CharField(max_length=30, default='-')
    estado = models.BooleanField(default=True)


class Zonas(models.Model):
    nombre = models.CharField(max_length=6)
    # alguna referencia de donde es la zona? o eso se considera manualmente
    # barrios que incluye??


class Clientes(models.Model):
    nombre = models.CharField(max_length=30)
    apellido = models.CharField(max_length=30)
    telefono = models.CharField(max_length=13)
    fecAlta = models.DateField(default=date.today)
    dni = models.CharField(max_length=8, unique=True)
    email = models.CharField(max_length=30, default='-', unique=True)
    fecnac = models.DateField(default=date.today)
    estado = models.BooleanField(default=True)
    # se podria considerar el empleado q lo cargo


class Insumos(models.Model):
    codigo = models.IntegerField()
    nombre = models.CharField(max_length=30, default='-')
    descripcion = models.CharField(max_length=60, default='-')
    existenciamin = models.IntegerField(default=0)
    estado = models.BooleanField(default=True)
    tipo = models.CharField(max_length=20)
    otro = models.FloatField(default=0)


class Depositos(models.Model):
    ubicacion = models.CharField(max_length=15)


class Contenido(models.Model):
    nom_cont = models.CharField(max_length=30)


class Det_Contenido(models.Model):
    cont_id = models.ForeignKey(Contenido)
    nom_ins = models.CharField(max_length=20)
    cantidad = models.FloatField()


class Articulos(models.Model):
    nombre = models.CharField(max_length=20, default='-')
    envase = models.CharField(max_length=10)
    capacidad = models.FloatField()
    contenido = models.ForeignKey(Contenido)
    existenciamin = models.IntegerField(default=0)
    estado = models.BooleanField(default=True)
    precio = models.FloatField(default=0.0)


class Camiones(models.Model):
    fecAdquisicion = models.DateField()
    estado = models.CharField(max_length=20)
    # estado del camion: reparacion, disponible, en servicio


class Empleado_Zona(models.Model):
    zona_id = models.ForeignKey(Zonas)
    emp_id = models.ForeignKey(Empleados)
    fecInicio = models.DateField()
    fecFin = models.DateField()


class StockInsumos(models.Model):
    ins_id = models.ForeignKey(Insumos)
    dep_id = models.ForeignKey(Depositos)
    cantidad = models.IntegerField(default=0)


class StockArticulos(models.Model):
    art_id = models.ForeignKey(Articulos)
    dep_id = models.ForeignKey(Depositos)
    cantidad = models.IntegerField(default=0)


class StockCamion(models.Model):
    art_id = models.ForeignKey(Articulos)
    emp_id = models.ForeignKey(Empleados)
    cantidad = models.IntegerField(default=0)


class NecesidadCamion(models.Model):
    art_id = models.ForeignKey(Articulos)
    emp_id = models.ForeignKey(Empleados)
    cantidad = models.IntegerField(default=0)


class Domicilios(models.Model):
    cli_id = models.ForeignKey(Clientes, on_delete=models.CASCADE)
    latitud = models.CharField(max_length=50, default='')
    longitud = models.CharField(max_length=50, default='')
    direccion = models.CharField(max_length=30, unique=True)


class Pedidos(models.Model):
    emp_id = models.ForeignKey(Empleados)
    rep_id = models.ForeignKey(Empleados, related_name='repartidor', default=0)
    cli_id = models.ForeignKey(Clientes)
    direccion = models.ForeignKey(Domicilios, default=0)
    formapago = models.CharField(max_length=10, default='Efectivo')
    fecha = models.DateField(default=date.today)
    fecha_entrega = models.DateField()
    total = models.FloatField(default=0.0)
    estado = models.BooleanField(default=False)


class Detalle_Pedido(models.Model):
    ped_id = models.ForeignKey(Pedidos)
    art_id = models.ForeignKey(Articulos)
    cantidad = models.IntegerField(default=0)


class VentaSinPedido(models.Model):
    rep_id = models.ForeignKey(Empleados, related_name='repartidorventa', default=0)
    cli_id = models.ForeignKey(Clientes)
    direccion = models.ForeignKey(Domicilios, default=0)
    formapago = models.CharField(max_length=10, default='Efectivo')
    total = models.FloatField(default=0.0)


class Ventas(models.Model):
    pedido = models.ForeignKey(Pedidos, default=0)
    sinpedido = models.ForeignKey(VentaSinPedido, default=0)
    fecha = models.DateField(default=date.today)


class Detalle_Venta(models.Model):
    venta = models.ForeignKey(VentaSinPedido, default=0)
    art = models.ForeignKey(Articulos, default=0)
    cantidad = models.IntegerField(default=0)
    subtotal = models.FloatField(default=0.0)


class Proveedores(models.Model):
    nombre = models.CharField(max_length=30)
    direccion = models.CharField(max_length=30)
    telefono = models.CharField(max_length=13)
    cuit = models.CharField(max_length=13, unique=True)
    cuentacorriente=models.CharField(max_length=15, default='-')
    envios=models.BooleanField(default=False)
    estado = models.BooleanField(default=True)


class Insumo_Proveedor(models.Model):
    ins_id = models.ForeignKey(Insumos)
    prov_id = models.ForeignKey(Proveedores)
    precio_ult_comp = models.CharField(max_length=50)


class Articulo_Proveedor(models.Model):
    art_id = models.ForeignKey(Articulos)
    prov_id = models.ForeignKey(Proveedores)
    precio_ult_comp = models.CharField(max_length=50)


class Det_Rec_Ins(models.Model):
    art_id = models.ForeignKey(Articulos)
    ins_id = models.ForeignKey(Insumos)


class Facturas(models.Model):
    prov_id = models.ForeignKey(Proveedores)
    fecha_recib = models.DateField()


class Remitos(models.Model):
    prov_id = models.ForeignKey(Proveedores)
    fecha_recib = models.DateField(default=date.today)
    codigo = models.IntegerField()
    

class Detalle_Remito(models.Model):
    rem_id = models.ForeignKey(Remitos)
    ins_id = models.ForeignKey(Insumos)
    cant_recib = models.IntegerField()
    vencimiento = models.DateField(default=date.today)
    dep_id = models.ForeignKey(Depositos)

class Copia_Remitos(models.Model):
    prov_id2 = models.ForeignKey(Proveedores)
    fecha_recib2 = models.DateField(default=date.today)
    codigo2 = models.IntegerField()

class Copia_DetRem(models.Model):
    rem_id2= models.IntegerField()
    ins_id2 = models.ForeignKey(Insumos)
    cant_recib2 = models.IntegerField()
    vencimiento2 = models.DateField(default=date.today)
    codigo2 = models.IntegerField()
    dep_id2 = models.ForeignKey(Depositos)


class Detalle_Factura(models.Model):
    fact_id = models.ForeignKey(Facturas)
    ins_id = models.ForeignKey(Insumos)
    cant_recib = models.IntegerField()
    precio_unit = models.CharField(max_length=50)


class Detalle_Produccion(models.Model):
    fecha_reg = models.DateField(default=date.today)
    cantidad = models.IntegerField(default=0)
    capacidad = models.FloatField(default=0)
    articulo_reg = models.ForeignKey(Articulos)
    tipo_reg = models.IntegerField(default=0)
    deposito = models.IntegerField(default=0)
    fecha_vto = models.DateField(default=date.today)
    fecha_env = models.DateField(default=date.today)
    lote = models.IntegerField(default=0)


class Copia_DetProd(models.Model):
    fecha_reg2 = models.DateField(default=date.today)
    cantidad2 = models.IntegerField(default=0)
    capacidad2 = models.FloatField(default=0)
    articulo_reg2 = models.IntegerField(default=0)
    tipo_reg2 = models.IntegerField(default=0)
    deposito2 = models.IntegerField(default=0)
    estado_reg2 = models.BooleanField(default=True)
    fecha_vto2 = models.DateField(default=date.today)
    fecha_env2 = models.DateField(default=date.today)
    lote2 = models.IntegerField(default=0)


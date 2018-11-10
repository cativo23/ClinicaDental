from django.db import models
from myauth import models as authModels
import datetime
from decimal import Decimal

# Create your models here.
class Producto(models.Model):
    nombre_producto = models.CharField('Nombre del producto', max_length = 30, blank = False, null = False)
    marca_producto = models.CharField('Marca del producto', max_length = 30, blank = False, null = False)
    existencia_producto = models.IntegerField('Exitencias', blank = False, null = False)
    precio_producto = models.DecimalField('Precio', max_digits=5, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return self.nombre_producto + ", " + self.marca_producto

    class meta:
        ordering = ['existencia_producto']
        verbose_name = 'producto'
        verbose_name_plural = 'productos'
        unique_together = (("nombre_producto", "marca_producto", "precio_producto"))


class Transaccion(models.Model):
    entrada = "ENTRADA"
    salida = "SALIDA"

    tipo_choices = (
        (entrada, 'ENTRADA'),
        (salida, 'SALIDA')
    )

    producto = models.ForeignKey(Producto, on_delete = models.PROTECT)
    tipo_transaccion = models.CharField('Tipo de registro', max_length = 7, choices = tipo_choices, blank= False, null= False )
    fecha = models.DateField('Fecha de registro',  help_text='Formato: AAAA-MM-DD', blank=False, null=False)
    cantidad = models.IntegerField('Cantidad', blank = False, null = False)

class Registro(models.Model):
    COMPRA = "compra"
    VENTA = "venta"
    CADUCO =  "caduco"
    REGISTRO_CHOICES = (
        (COMPRA, 'Compra'),
        (VENTA, 'Venta'),
        (CADUCO, 'Caduco'),
    )
    producto = models.ForeignKey(Producto, on_delete = models.PROTECT)
    tipo_registro = models.CharField('Tipo de registro', max_length = 10, choices = REGISTRO_CHOICES, blank = False, null = False)
    cantidad_registro = models.IntegerField('Cantidad', blank = False, null = False)
    fecha_registro = models.DateField('Fecha de registro',  help_text='Formato: AAAA-MM-DD', blank=False, null=False)

    class meta:
        ordering = ['fecha_registro']
        verbose_name = 'registro'
        verbose_name_plural = 'registros'
        unique_together = (("", ""),)

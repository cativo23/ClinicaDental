from django.db import models
import GestionExpedientes


class Pago(models.Model):
    Expediente = models.ForeignKey('GestionExpedientes.Expediente', on_delete = models.CASCADE, null = True, blank= False)
    fechaPago= models.DateTimeField('Fecha de Pago', auto_now_add=True)
    cantidad = models.DecimalField(max_digits=5, decimal_places=2, blank=False, null=False, default=0)

    def __str__(self):
        return '#%s - Pago por: %s del %s' % (self.id, self.cantidad ,self.expediente)

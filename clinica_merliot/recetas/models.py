from django.db import models
import odontograma

# Create your models here.

class Medicamento(models.Model):
    nombre_medicamento = models.CharField('Nombre del medicamento', max_length = 45, blank = False, null = False)
    marca_medicamento = models.CharField('Nombre del producto', max_length = 45, blank = False, null = False)
    presentacion_medicamento = models.CharField('Nombre del producto', max_length = 45, blank = False, null = False)
    form_farmaceutica = models.CharField('Nombre del producto', max_length = 45, blank = False, null = False)

    class meta:
        ordering = ['nombre_medicamento']
        verbose_name = 'medicamento'
        verbose_name_plural = 'medicamentos'
        unique_together = (("nombre_medicamento", "marca_medicamento", "presentacion_medicamento"))

class Receta(models.Model):
    consulta = models.ForeignKey('odontograma.Consulta', on_delete=models.PROTECT)
    medicamento = models.ManyToManyField(Medicamento, through='Especificacion')


class Especificacion(models.Model):
    medicamento = models.ForeignKey(Medicamento, on_delete=models.CASCADE)
    receta = models.ForeignKey(Receta, on_delete=models.CASCADE)
    dosis = models.CharField('Dosis', max_length = 45, blank = False, null = False)
    duracion = models.CharField('Duracion', max_length = 45, blank = False, null = False)

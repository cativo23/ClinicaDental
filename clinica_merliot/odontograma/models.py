from django.db import models
import GestionExpedientes
from django.utils import timezone as tz



#from GestionExpedientes.models import  Doctor, Paciente
# Create your models here.

class Odontograma(models.Model):
    medico = models.ForeignKey('GestionExpedientes.Doctor', on_delete = models.SET_NULL, null = True)
    fechaCreacion = models.DateTimeField('date_created', auto_now_add=True)
    notas = models.TextField()

    def __str__(self):
        return '#%s - Ondontograma del %s' % (self.id, GestionExpedientes.models.Expediente.objects.filter(odontograma=self.id).first())

class Tratamiento(models.Model):
    nombreTratamiento = models.CharField('Nombre del tratamiento', max_length=100, blank=False, null=False)
    descripcionTratamiento = models.TextField('Descripcion del tratamiento', max_length=250, blank=True, null=True)
    precioBase = models.DecimalField('Precio Base', max_digits=5, decimal_places=2)

    def __str__(self):
        return self.nombreTratamiento

    class Meta:
        ordering = ['nombreTratamiento']
        verbose_name = 'Tratamiento'
        verbose_name_plural = 'Tratamientos'


class Procedimiento(models.Model):
    CARAS_CHOICES = (
        ('S', 'Vestibular'),
        ('C', 'Oclusal'),
        ('X', 'Pieza Completa'),
        ('Z', 'Distal'),
        ('D', 'Mesial'),
        ('I', 'Palatino'),
    )
    STATUS_CHOICES = (
        ('recomendado', 'Recomendado'),
        ('autorizado', 'Autorizado'),
        ('en_proceso', 'En Proceso'),
        ('completado', 'Completado')
    )

    pieza = models.IntegerField()
    cara = models.CharField(max_length=4, choices=CARAS_CHOICES)
    tratamiento = models.ForeignKey(Tratamiento, on_delete = models.CASCADE)
    odontograma = models.ForeignKey(Odontograma, on_delete = models.CASCADE)
    diagnostico = models.TextField()
    notas = models.TextField(blank=True)
    status = models.CharField(
        max_length=12, choices=STATUS_CHOICES, default='recomendado')

    def __str__(self):
        return self.tratamiento.nombreTratamiento


class Consulta(models.Model):
    doctor = models.ForeignKey('GestionExpedientes.Doctor', on_delete=models.PROTECT)
    paciente = models.ForeignKey('GestionExpedientes.Expediente', on_delete=models.PROTECT)
    fechaConsulta = models.DateField('Fecha de Consulta', default=tz.now)
    horaInicio = models.TimeField('Hora de inicio', auto_now_add=True)
    horaFinal = models.TimeField('Hora de Final', auto_now_add=False, null=True)
    observacionCons = models.TextField('Observaciones', max_length=250, blank=True, null=True)

    def __str__(self):
        return 'Consulta de {} del dia {}'.format(self.paciente.paciente.nombresPaciente, self.fechaConsulta)

    class Meta:
        ordering = ['fechaConsulta', 'horaInicio']
        verbose_name = 'Consulta'
        verbose_name_plural = 'Consultas'

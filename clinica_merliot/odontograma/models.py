from django.db import models
from GestionExpedientes.models import Tratamiento, Doctor, Paciente
# Create your models here.

class Odontograma(models.Model):
    medico = models.ForeignKey(Doctor, on_delete = models.SET_NULL, null = True)
    paciente = models.ForeignKey(Paciente, on_delete = models.CASCADE)
    notas = models.TextField()

    def __str__(self):
        return '%s - %s' % (self.id, self.evaluacion)

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
        return unicode(self.tratamiento)

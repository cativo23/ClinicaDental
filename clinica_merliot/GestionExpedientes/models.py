from django.db import models
from myauth import models as authModels
import datetime
from decimal import Decimal
# Create your models here.


class Doctor(models.Model):
    usuario = models.OneToOneField(authModels.MyUser, on_delete=models.CASCADE)
    nombreDoctor = models.CharField('Nombre', max_length=60, blank=False, null=False)
    esDuenio = models.BooleanField(' Es la duenia? ', default=False)

    def __str__(self):
        return "Dra. " + self.nombreDoctor

    class Meta:
        ordering = ['nombreDoctor']
        verbose_name = 'Doctor(a)'
        verbose_name_plural = 'Doctor(a)s'


class Paciente(models.Model):
    MASCULINO = 'M'
    FEMENINO = "F"
    SEXO_CHOICES = (
        (MASCULINO, 'Masculino'),
        (FEMENINO, 'Femenino'),
    )
    nombresPaciente = models.CharField('Nombres del paciente', max_length=60, blank=False, null=False)
    apellidosPaciente = models.CharField(max_length=60, blank=False, null=False)
    ocupacion = models.CharField(max_length=60, blank=True, null=True)
    sexo = models.CharField(max_length=2, choices=SEXO_CHOICES, default=None, blank=False, null=False)
    fechaNacimiento = models.DateField('Fecha de nacimiento',  help_text='Formato: AAAA-MM-DD', blank=False, null=False)
    direccionCasa = models.CharField('Direccion Casa', max_length=150, blank=True, null=True)
    direccionTrabajo = models.CharField('Direccion Trabajo', max_length=150, blank=True, null=True)
    telefonoCasa = models.CharField('Telefono Casa', max_length=9, help_text='Formato: XXXX-XXXX', blank=True, null=True)
    telefonoTrabajo = models.CharField('Telefono Trabajo', max_length=9, help_text='Formato: XXXX-XXXX', blank=True, null=True)
    referencia = models.CharField('Responsable', max_length=60, help_text='(En caso de ser ninio)', blank=True, null=True)

    def __str__(self):
        return self.apellidosPaciente + ", " + self.nombresPaciente

    class Meta:
        ordering = ['apellidosPaciente', 'nombresPaciente']
        unique_together = (("nombresPaciente", "apellidosPaciente"),)
        verbose_name = 'Paciente'
        verbose_name_plural = 'Pacientes'


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


class Expediente(models.Model):
    paciente = models.OneToOneField(Paciente, on_delete=models.CASCADE)
    tratamientos = models.ManyToManyField(Tratamiento, blank=True)
    fechaCreacion = models.DateTimeField('date_created', auto_now_add=True)
    pagado = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    saldo = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    observacionExp = models.TextField('Observaciones', max_length=250, blank=True, null=True)

    def __str__(self):
        return "Expediente de " + self.paciente.apellidosPaciente + ", " + self.paciente.nombresPaciente

    class Meta:
        ordering = ['paciente']
        verbose_name = 'Expediente'
        verbose_name_plural = 'Expedientes'


class Consulta(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.PROTECT)
    paciente = models.ForeignKey(Expediente, on_delete=models.PROTECT)
    fechaConsulta = models.DateField('Fecha de Consulta', auto_now_add=True)
    horaInicio = models.TimeField('Hora de inicio', auto_now_add=True)
    horaFinal = models.TimeField('Hora de Final', auto_now_add=False, null=True)
    observacionCons = models.TextField('Observaciones', max_length=250, blank=True, null=True)

    def __str__(self):
        return 'Consulta de {} del dia {}'.format(self.paciente.paciente.nombresPaciente, self.fechaConsulta)

    class Meta:
        ordering = ['fechaConsulta', 'horaInicio']
        verbose_name = 'Consulta'
        verbose_name_plural = 'Consultas'

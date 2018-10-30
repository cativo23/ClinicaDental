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
        if self.usuario.sex == "M":
            return "Dr. " + self.nombreDoctor
        else:
            return "Dra. " + self.nombreDoctor


    class Meta:
        ordering = ['nombreDoctor']
        verbose_name = 'Doctor'
        verbose_name_plural = 'Doctores'


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
    fechaNacimiento = models.DateField('Fecha de nacimiento', help_text='Formato: DD-MM-AAAA', blank=False, null=False)
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


class Expediente(models.Model):
    paciente = models.OneToOneField(Paciente, on_delete=models.CASCADE)
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



class Cita(models.Model):
    APLICADA = 'Aplicada'
    PENDIENTE = "Pendiente"
    NO_ASISTIO = 'No Asistio'
    ESTADO_CHOICES = (
        (APLICADA, 'Aplicada'),
        (PENDIENTE, 'Pendiente'),
        (NO_ASISTIO,'No Asistio'),
        )
    asuntoCita=models.CharField('Asunto de la cita', max_length=50,blank=False,null=False)
    paciente = models.ForeignKey(Expediente, on_delete=models.PROTECT)
    doctor = models.ForeignKey(Doctor, on_delete=models.PROTECT)
    fechaCita = models.DateField('Fecha de Cita', help_text='Formato: AAAA-MM-DD', blank=False, null=False)
    horaCita = models.TimeField('Hora de Cita', blank=False, null=False)
    observacionCita = models.TextField('Observaciones', max_length=250, blank=True, null=True)
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default=None, blank=False, null=False)
    

    def __str__(self):
        return 'Cita de {} el dia {}'.format(self.paciente.paciente.nombresPaciente, self.fechaCita)

    class Meta:
        ordering = ['fechaCita', 'horaCita']
        verbose_name = 'Cita'
        verbose_name_plural = 'Citas'



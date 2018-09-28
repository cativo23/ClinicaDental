from django.contrib import admin

from .models import Doctor, Expediente, Paciente, Cita


# Register your models here.

admin.site.register(Doctor)
admin.site.register(Expediente)
admin.site.register(Paciente)
admin.site.register(Cita)


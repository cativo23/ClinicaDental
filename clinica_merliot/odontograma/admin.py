from django.contrib import admin
from .models import Odontograma, Procedimiento, Tratamiento, Consulta

# Register your models here.

admin.site.register(Odontograma)
admin.site.register(Procedimiento)
admin.site.register(Tratamiento)
admin.site.register(Consulta)

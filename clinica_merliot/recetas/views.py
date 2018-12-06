from django.shortcuts import render

from .forms import nuevoMedicamentoForm, nuevaEspecificacionForm
from .models import Medicamento
from django.contrib import messages

# Create your views here.

def principalRecetas(request):
    return render(request, 'recetas/principalReceta.html', {})

def principalMedicamento(request):

    queryset_medicamento = Medicamento.objects.all()
    form_medicamento = nuevoMedicamentoForm()

    context = {
        'object_list':queryset_medicamento,
        'form_medicamento':form_medicamento,
    }

    if request.method == 'POST':
        form_medicamento = nuevoMedicamentoForm(request.POST)
        if form_medicamento.is_valid():
            form_medicamento.save()
            messages.success(request, "El medicamento fue agregado correctamente!")
        else:
            print('No fue valida')
        form_medicamento = nuevoMedicamentoForm()
        messages.warning(request, "ERROR!")
        return render(request,'recetas/principalMedicamento.html' , context)
    return render(request, 'recetas/principalMedicamento.html', context)

def asignandoReceta(request):

    form_especificacion = nuevaEspecificacionForm()

    context = {
        'form_especificacion':form_especificacion,
    }

    return render(request, 'recetas/asignarReceta.html', context)

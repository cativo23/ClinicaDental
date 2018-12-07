from django.shortcuts import render

from .forms import nuevoMedicamentoForm, nuevaEspecificacionForm
from .models import Medicamento, Receta, Especificacion
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
    if request.method =='POST':
        form_especificacion = nuevaEspecificacionForm(request.POST)
        if form_especificacion.is_valid():
            nuevaReceta=Receta.objects.latest('id')

            e = Especificacion(
                dosis=form_especificacion.cleaned_data['dosis'],
                duracion=form_especificacion.cleaned_data['duracion'],
                receta=nuevaReceta,
                medicamento=form_especificacion.cleaned_data['medicamento']
                )
            e.save()

            form_especificacion = nuevaEspecificacionForm()
            listaMed = nuevaReceta.medicamento.all()

            context = {
                'form_especificacion': form_especificacion,
                'object_list': listaMed,
            }
            return render(request, 'recetas/asignarReceta.html', context)

    form_especificacion = nuevaEspecificacionForm()
    context = {
        'form_especificacion': form_especificacion,
    }

    return render(request, 'recetas/asignarReceta.html', context)

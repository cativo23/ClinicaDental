from django.shortcuts import render

from datetime import datetime

from django.contrib.auth.decorators import permission_required
from django.shortcuts import redirect, get_object_or_404, render
from django.views.generic import UpdateView, DetailView
from GestionExpedientes.models import Tratamiento, Doctor, Paciente
from .models import Odontograma

from .forms import OdontogramaForm, ProcedimientoFormSet
# Create your views here.

def odontograma(request, paciente_id):
    '''
    Crea Odontograma con Procedimientos. Se generará una cotizacion despues
    de esto.
    '''
    template = 'Odonto/testOdonto.html'
    paciente = get_object_or_404(Paciente, pk=paciente_id)
    tratamientos = Tratamiento.objects.all()
    medico = get_object_or_404(Doctor, pk = request.user.doctor.pk)
    # initial = [{
    #     'pieza': None,
    #     'cara': None,
    #     'tratamiento': None,
    #     'diagnostico': None,
    #     'notas': None,
    # }]
    initial = [{}]

    if request.method == 'POST':
        modelform = OdontogramaForm(request.POST)
        formset = ProcedimientoFormSet(request.POST, initial=initial)

        if modelform.is_valid():
            odontograma = modelform.save(commit=False)
            odontograma.paciente = paciente
            odontograma.medico = medico
            odontograma.save()
            print(formset)
            if formset.is_valid():
                for form in formset:
                    form.instance.odontograma = odontograma
                    form.save()

            #    try:
                    #cotizacion = odontograma.cotizacion_set.get()

            #    except Cotizacion.DoesNotExist:
                    #cotizacion = Cotizacion.objects.create(
            #            odontograma=odontograma)
            #        CotizacionItem.objects.create_items(cotizacion)

                return redirect(reverse(
                    'clinica:odontograma_detail', args=[odontograma.id]))

    else:
        modelform = OdontogramaForm()
        formset = ProcedimientoFormSet(initial=initial)

    # print len(formset)
    print (formset.initial_form_count())
    print (formset.total_form_count())
    # for form in formset:
    #     print '*' * 20
    #     print form

    return render(request, template, {
                  'form': modelform,
                  'formset': formset,
                  'paciente': paciente,
                  'tratamientos': tratamientos,
                  'o_active': 'active'
                  })


class OdontogramaDetail(DetailView):
    model = Odontograma
    context_object_name = 'odontograma'
    template_name = 'odontograma-detail.html'
    permission_required = 'clinica.add_odontograma'

    def get_context_data(self, **kwargs):
        context = super(OdontogramaDetail, self).get_context_data(**kwargs)
        paciente = self.object.paciente
        procedimientos = self.object.procedimiento_set.all()
        context.update({'paciente': paciente,
                        'procedimientos': procedimientos,
                        'o_active': 'active'})
        return context

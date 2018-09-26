from django.shortcuts import render

from datetime import datetime

from django.contrib.auth.decorators import permission_required
from django.core.urlresolvers import reverse
from django.shortcuts import redirect, get_object_or_404, render
from django.views.generic import UpdateView, DetailView

# Create your views here.

def odontograma(request, paciente_id):
    '''
    Crea Odontograma con Procedimientos. Se generará una cotizacion despues
    de esto.
    '''
    paciente = get_object_or_404(Paciente, pk=paciente_id)
    tratamientos = Tratamiento.objects.all()
    medico = request.user.medico_set.get()
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

            if formset.is_valid():
                for form in formset:
                    form.instance.odontograma = odontograma
                    form.save()

                try:
                    cotizacion = odontograma.cotizacion_set.get()

                except Cotizacion.DoesNotExist:
                    cotizacion = Cotizacion.objects.create(
                        odontograma=odontograma)
                    CotizacionItem.objects.create_items(cotizacion)

                return redirect(reverse(
                    'clinica:odontograma_detail', args=[odontograma.id]))

        # TODO: agregar form vacio

    else:
        modelform = OdontogramaForm()
        formset = ProcedimientoFormSet(initial=initial)

    # print len(formset)
    print formset.initial_form_count()
    print formset.total_form_count()
    # for form in formset:
    #     print '*' * 20
    #     print form

    return render(request, 'odontograma.html', {
                  'form': modelform,
                  'formset': formset,
                  'paciente': paciente,
                  'tratamientos': tratamientos,
                  'o_active': 'active'
                  })


class OdontogramaDetail(PermissionRequiredMixin, DetailView):
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

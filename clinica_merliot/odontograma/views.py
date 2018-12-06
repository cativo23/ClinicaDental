from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, TemplateView
from django.views.generic.detail import DetailView
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from django.shortcuts import get_object_or_404
from datetime import date, datetime
from django.urls import reverse

from django.contrib.auth.decorators import permission_required
from django.shortcuts import redirect, get_object_or_404, render
from django.views.generic import UpdateView, DetailView
from GestionExpedientes.models import Doctor, Paciente, Expediente
from .models import Odontograma, Procedimiento, Tratamiento, Consulta
from GestionExpedientes.forms import nuevoExpedienteForm

from .forms import OdontogramaForm, ProcedimientoFormSet, NuevaConsultaForm,  nuevoTratamientoForm, ConsultaForm
import traceback
import math
# Create your views here.

def odontograma(request, paciente_id):
    '''
    Crea Odontograma con Procedimientos. Se generará una cotizacion despues
    de esto.
    '''
    template = 'Odonto/testOdonto.html'
    expediente = get_object_or_404(Expediente, pk=1)
    paciente = get_object_or_404(Paciente, pk=expediente.paciente.id)
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
        formset = ProcedimientoFormSet(request.POST)

        if modelform.is_valid():
            odontograma = modelform.save(commit=False)
            odontograma.paciente = paciente
            odontograma.medico = medico
            odontograma.save()
            expediente.odontograma = odontograma
            expediente.save()
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

                return redirect(reverse('odontograma:odontograma_detail', args=[odontograma.id]))

    else:
        modelform = OdontogramaForm()
        formset = ProcedimientoFormSet(initial=initial)

    return render(request, template, {
                  'form': modelform,
                  'formset': formset,
                  'paciente': paciente,
                  'tratamientos': tratamientos,
                  'o_active': 'active'
                  })


class OdontogramaDetail(DetailView):
    slug_field = 'id'
    model = Odontograma
    context_object_name = 'odontograma'
    template_name = 'Odonto/odontograma-detail.html'

    def get_context_data(self, **kwargs):
        context = super(OdontogramaDetail, self).get_context_data(**kwargs)
        paciente = self.object.expediente
        procedimientos = self.object.procedimiento_set.all()
        fecha = self.object.fechaCreacion
        context.update({'paciente': paciente,
                        'procedimientos': procedimientos,
                        'fecha' : fecha,
                        'o_active': 'active'})
        return context


class ProcedimientoDetail( DetailView):
    model = Procedimiento
    template_name = 'Odonto/detalleConsulta.html'
    slug_field = 'id'
    slug_url_kwarg = 'id'


class TratamientoDetail(LoginRequiredMixin, DetailView):
    model = Tratamiento
    template_name = 'GestionExpedientes/detalleTratamiento.html'
    slug_field = 'id'
    slug_url_kwarg = 'id'


class TratamientoList(LoginRequiredMixin, ListView):
    model = Tratamiento
    template_name = 'GestionExpedientes/listaTratamientos.html'
    ordering = 'nombreTratamiento'

    def get_queryset(self):
        qs = Tratamiento.objects.all()

        keywords = self.request.GET.get('q')
        if keywords:
            query = SearchQuery(keywords)
            vector = SearchVector('nombreTratamiento',)
            qs = qs.annotate(search=vector).filter(search=query)
            qs = qs.annotate(rank=SearchRank(vector, query)).order_by('-rank')

        return qs


@login_required
def editarTratamiento(request, pk):
    template = 'GestionExpedientes/editarTratamiento.html'
    tratamiento = get_object_or_404(Tratamiento, pk=pk)

    if request.method == 'POST':
        form = nuevoTratamientoForm(request.POST, instance = tratamiento)

        try:
            if form.is_valid():
                form.save()
                messages.success(request, "El tratamiento fue modificado correctamente!")
                return redirect('odontograma:listarTratamientos')

        except Exception as e:
            messages.warning(request, 'Your Post Was Not Saved Due To An Error: {}'.format(e))
    else:
        form = nuevoTratamientoForm(instance=tratamiento)

    context = {
        'form': form,
        'tratamiento': tratamiento
    }

    return render(request, template, context)


class ConsultasList(LoginRequiredMixin, ListView):
    model = Consulta
    template_name = 'GestionExpedientes/consultas.html'
    ordering = '-paciente'

    def get_queryset(self):
        qs = Consulta.objects.all()

        keywords = self.request.GET.get('q')
        if keywords:
            query = SearchQuery(keywords)
            vector = SearchVector('paciente__paciente__nombresPaciente', 'paciente__paciente__apellidosPaciente', 'doctor__nombreDoctor')
            qs = Consulta.objects.annotate(search=vector).filter(search=query)
            qs = qs.annotate(rank=SearchRank(vector, query)).order_by('-rank')

        return qs


class ConsultaDetail(LoginRequiredMixin, DetailView):
    model = Consulta
    template_name = 'GestionExpedientes/detalleConsulta.html'
    slug_field = 'id'
    slug_url_kwarg = 'id'


@login_required
def consulta(request, pk):
    template = 'GestionExpedientes/consulta.html'
    consulta = get_object_or_404(Consulta, pk=pk)
    consulta.doctor = request.user.doctor
    tratamientos = Tratamiento.objects.all()
    medico = get_object_or_404(Doctor, pk = request.user.doctor.pk)
    expediente = get_object_or_404(Expediente, pk=consulta.paciente.id)
    edad = (date.today() - expediente.paciente.fechaNacimiento).days/365
    ed = math.trunc(edad)

    initial = [{}]
    odontograma = Odontograma.objects.get(id= expediente.odontograma.id)

    if request.method == 'POST':
        try:
            if 'odoform' in request.POST:
                form = ConsultaForm(instance=consulta)
                formset = ProcedimientoFormSet(request.POST, initial=initial)
                modelform = OdontogramaForm(request.POST, instance = odontograma)
                if modelform.is_valid():
                    odontograma = modelform.save(commit=False)
                    odontograma.medico = medico
                    odontograma.save()
                    if formset.is_valid():
                        for form in formset:
                            form.instance.odontograma = odontograma
                            form.save()
                    messages.success(request, "El odonto se guardo Correctamente!")
                    form = ConsultaForm(instance=consulta)
                    return redirect('odontograma:verConsulta', pk=pk)
                else:
                    print('ERROR: {}'.format(modelform.errors))
                form = ConsultaForm(instance=consulta)
            elif 'consform' in request.POST:
                form = ConsultaForm(request.POST, instance=consulta)
                if form.is_valid():
                    if consulta.horaFinal == None:
                        form.instance.horaFinal = datetime.now()
                    form.save()
                    messages.success(request, "La consulta fue modificada correctamente!")
                    return redirect('odontograma:listarConsultas')
                else:
                    print('ERROR CONSULTA: {}'.format(form.errors))
        except Exception as e:
            messages.error(request, 'Error: %s'%e)
            traceback.print_tb(e.__traceback__)
    else:
        form = ConsultaForm(instance=consulta)
        formset = ProcedimientoFormSet(initial=initial)
        modelform = OdontogramaForm(instance = odontograma)

    context = {
        'form': form,
        'consulta': consulta,
        'expediente': expediente,
        'edad': ed,
        'forms': modelform,
        'formset': formset,
        'paciente': expediente,
        'tratamientos': tratamientos,
        'o_active': 'active'
    }
    return render(request, template, context)


@login_required
def agregarConsulta(request):
    template = 'GestionExpedientes/agregarConsulta.html'
    if request.method == 'POST':
        form = NuevaConsultaForm(request.POST)
        try:
            if form.is_valid():
                consulta = form.save()
                messages.success(request, "La consulta fue creada correctamente!")
                return redirect('odontograma:verConsulta', consulta.id )
        except Exception as e:
            messages.warning(request, 'Your Post Was Not Saved Due To An Error: {}'.format(e))
    else:
        data = {'doctor': request.user.doctor}
        form = NuevaConsultaForm(initial = data)

    context = {
        'form': form
    }

    return render(request, template, context)


@login_required
def agregarTratamiento(request):
    if request.method == 'POST':
        form = nuevoTratamientoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tratamiento correctamente guardado!')
            return redirect('odontograma:listarTratamientos')
    else:
        form = nuevoTratamientoForm()
    return render(request, 'GestionExpedientes/agregarTratamiento.html', {'form': form, })


class OdontogramaList(LoginRequiredMixin, ListView):
    model = Odontograma
    template_name = 'Odonto/odos.html'
    ordering = '-fechaCreacion'
    slug_field = 'id'

    def get_queryset(self):

        qs = Odontograma.objects.filter(paciente=self.kwargs['slug'])

        keywords = self.request.GET.get('q')
        if keywords:
            query = SearchQuery(keywords)
            vector = SearchVector('paciente__nombresPaciente', 'paciente__paciente__apellidosPaciente', 'doctor__nombreDoctor')
            qs = Consulta.objects.annotate(search=vector).filter(search=query)
            qs = qs.annotate(rank=SearchRank(vector, query)).order_by('-rank')

        return qs


    def get_context_data(self, **kwargs):
        context = super(OdontogramaList, self).get_context_data(**kwargs)
        paciente = get_object_or_404(Paciente, pk=self.kwargs['slug'])

        context.update({'paciente': paciente,
                        })
        return context

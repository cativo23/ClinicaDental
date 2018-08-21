from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .forms import nuevoExpedienteForm, nuevoTratamientoForm, nuevoPacienteForm, ConsultaForm, ExpForm, NuevaConsultaForm
from django.contrib import messages
from .models import Expediente, Paciente, Tratamiento, Consulta
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, TemplateView
from django.views.generic.detail import DetailView
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from django.shortcuts import get_object_or_404
from datetime import datetime

# Create your views here.


@login_required
def index(request):
    return render(request, 'GestionExpedientes/index.html', {})


@login_required
def nuevoExpediente(request):
    if request.method == 'POST':
        form2 = nuevoPacienteForm(request.POST)
        form1 = ExpForm(request.POST)
        try:
            if form2.is_valid() and form1.is_valid():
                a = form2.save()
                b = form1.cleaned_data['observacionExp']
                expediente = Expediente.objects.create(paciente=a, observacionExp=b)
                if request.user.doctor is not None:
                    cons = Consulta.objects.create(paciente=expediente, doctor=request.user.doctor)
                    messages.success(request, 'Expediente correctamente guardado!')
                    return redirect('gestionExp:verConsulta', cons.id)
            else:
                print ('hola')
                return render(request, 'GestionExpedientes/nuevoExpediente.html', { 'form2': form2,})
        except Exception as e:
            messages.warning(request, 'Your Post Was Not Saved Due To An Error: {}'.format(e))
            return render(request, 'GestionExpedientes/nuevoExpediente.html', { 'form2': form2,})
    else:
        form2 = nuevoPacienteForm()
        form1 = ExpForm()
        return render(request, 'GestionExpedientes/nuevoExpediente.html', { 'form2': form2, 'form1': form1,})


@login_required
def agregarTratamiento(request):
    if request.method == 'POST':
        form = nuevoTratamientoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tratamiento correctamente guardado!')
            return redirect('GestionExpedientes:listarTratamientos')
    else:
        form = nuevoTratamientoForm()
    return render(request, 'GestionExpedientes/agregarTratamiento.html', {'form': form, })


class PacienteList(LoginRequiredMixin, ListView):
    model = Expediente
    template_name = 'GestionExpedientes/listaExpedientes.html'
    ordering = 'paciente'

    def get_queryset(self):
        qs = Expediente.objects.all()

        keywords = self.request.GET.get('q')
        if keywords:
            query = SearchQuery(keywords)
            vector = SearchVector('paciente__nombresPaciente', 'paciente__apellidosPaciente')
            qs = qs.annotate(search=vector).filter(search=query)
            qs = qs.annotate(rank=SearchRank(vector, query)).order_by('-rank')

        return qs


class PacienteDetail(LoginRequiredMixin, DetailView):
    model = Expediente
    template_name = 'GestionExpedientes/detalleExpediente.html'
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
                return redirect('gestionExp:listarTratamientos')

        except Exception as e:
            messages.warning(request, 'Your Post Was Not Saved Due To An Error: {}'.format(e))
    else:
        form = nuevoTratamientoForm(instance=tratamiento)

    context = {
        'form': form,
        'tratamiento': tratamiento
    }

    return render(request, template, context)


class Paciente2List(LoginRequiredMixin, ListView):
    model = Expediente
    template_name = 'GestionExpedientes/actualizarExpediente.html'
    ordering = 'paciente'

    def get_queryset(self):
        qs = Expediente.objects.all()

        keywords = self.request.GET.get('q')
        if keywords:
            query = SearchQuery(keywords)
            vector = SearchVector('paciente__nombresPaciente', 'paciente__apellidosPaciente')
            qs = qs.annotate(search=vector).filter(search=query)
            qs = qs.annotate(rank=SearchRank(vector, query)).order_by('-rank')

        return qs


@login_required
def editarExpediente(request, pk):
    template = 'GestionExpedientes/editarExpediente.html'
    expediente = get_object_or_404(Paciente, pk=pk)

    if request.method == 'POST':
        form = nuevoPacienteForm(request.POST, instance=expediente)
        form1 = ExpForm(request.POST, instance=expediente.expediente)
        try:
            if form.is_valid() and form1.is_valid():
                form.save()
                form1.save()
                messages.success(request, "El EXPEDIENTE FUE MODIFICADO CORRECTAMENTE!")
                return redirect('gestionExp:listar2Expedientes')

        except Exception as e:
            messages.warning(request, 'Your Post Was Not Saved Due To An Error: {}'.format(e))
    else:
        form = nuevoPacienteForm(instance=expediente)
        form1 = ExpForm(instance=expediente.expediente)

    context = {
        'form': form,
        'form1': form1,
        'expediente': expediente
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
    expediente = get_object_or_404(Expediente, pk=consulta.paciente.id)

    if request.method == 'POST':
        form = ConsultaForm(request.POST, instance=consulta)
        form1 = nuevoExpedienteForm(request.POST, instance=expediente)

        try:
            if form.is_valid() and form1.is_valid():
                consulta = form.save()
                consulta.horaFinal = datetime.now()
                form1.save()
                messages.success(request, "El la consulta fue modificada correctamente!")
                return redirect('gestionExp:listarConsultas')

        except Exception as e:
            messages.warning(request, 'Your Post Was Not Saved Due To An Error: {}'.format(e))
    else:
        form = ConsultaForm(instance=consulta)
        form1 = nuevoExpedienteForm(instance=expediente)

    context = {
        'form': form,
        'form1': form1,
        'consulta': consulta,
        'expediente': expediente
    }

    return render(request, template, context)


@login_required
def agregarConsulta(request):
    template = 'GestionExpedientes/agregarConsulta.html'
    if request.method == 'POST':
        form = NuevaConsultaForm(request.POST)

        try:
            print(form.is_valid())
            if form.is_valid():
                consulta = form.save()
                messages.success(request, "La consulta fue creada correctamente!")
                return redirect('gestionExp:verConsulta', consulta.id )

        except Exception as e:
            messages.warning(request, 'Your Post Was Not Saved Due To An Error: {}'.format(e))
    else:
        form = NuevaConsultaForm()

    context = {
        'form': form
    }

    return render(request, template, context)

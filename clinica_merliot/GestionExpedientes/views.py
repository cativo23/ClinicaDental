from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from .forms import nuevoExpedienteForm, nuevoPacienteForm, ExpForm, NuevaCitaForm
from django.contrib import messages
from .models import Expediente, Paciente,Cita

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, TemplateView
from django.views.generic.detail import DetailView
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from django.shortcuts import get_object_or_404
from datetime import date, datetime

from odontograma.models import Consulta, Odontograma
# Create your views here.

from django.utils import timezone
from django.shortcuts import render_to_response

from datetime import datetime
import json
from json import dumps


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
                odonto = Odontograma(medico=request.user.doctor)
                odonto.save()
                expediente = Expediente.objects.create(paciente=a, observacionExp=b, odontograma = odonto)

                if request.user.doctor is not None:
                    cons = Consulta.objects.create(paciente=expediente, doctor=request.user.doctor)
                    messages.success(request, 'Expediente correctamente guardado!')
                    return redirect('odontograma:verConsulta', cons.id)

            else:
                return render(request, 'GestionExpedientes/nuevoExpediente.html', { 'form2': form2, 'form1': form1,})
        except Exception as e:
            messages.warning(request, 'Your Post Was Not Saved Due To An Error: {}'.format(e))
            return render(request, 'GestionExpedientes/nuevoExpediente.html', { 'form2': form2, 'form1': form1,})

    else:
        form2 = nuevoPacienteForm()
        form1 = ExpForm()
        return render(request, 'GestionExpedientes/nuevoExpediente.html', { 'form2': form2, 'form1': form1,})



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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        fecha = Expediente.objects.get(id=self.kwargs['id']).paciente.fechaNacimiento
        print(fecha)
        hoy = date.today()
        print(hoy)
        edad = hoy.year - fecha.year - ((hoy.month, hoy.day) < (fecha.month, fecha.day))
        print(edad)
        context['ahorita'] = edad
        return context


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
                mes = "El expediente de %s fue modificado correctamente!"%expediente
                messages.success(request, mes)
                return redirect('gestionExp:listarExpedientes')

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


class CitaList(LoginRequiredMixin, ListView):
    model = Cita
    template_name = 'GestionExpedientes/cita.html'
    ordering = '-paciente'

    def get_queryset(self):
        qs = Cita.objects.all()

        keywords = self.request.GET.get('q')
        if keywords:
            query = SearchQuery(keywords)
            vector = SearchVector('paciente__paciente__nombresPaciente', 'paciente__paciente__apellidosPaciente', 'doctor__nombreDoctor')
            qs = Cita.objects.annotate(search=vector).filter(search=query)
            qs = qs.annotate(rank=SearchRank(vector, query)).order_by('-rank')

        return qs


class CitaDetail(LoginRequiredMixin, DetailView):
    model = Cita
    template_name = 'GestionExpedientes/detalleCita.html'
    slug_field = 'id'
    slug_url_kwarg = 'id'

@login_required
def agregarCita(request):
    template = 'GestionExpedientes/agregarCita.html'
    if request.method == 'POST':
        form = NuevaCitaForm(request.POST)
        print(form.errors)
        try:
            print(form.is_valid())
            if form.is_valid():
                cita = form.save()
                messages.success(request, "La cita fue creada correctamente!")
                return redirect('gestionExp:listarCita')

        except Exception as e:
            messages.error(request, 'La cita no se creo debido a un error: {}'.format(e))
    else:
        form = NuevaCitaForm()

    context = {
        'form': form
    }

    return render(request, template, context)

@login_required
def editarCita(request, pk):
    template = 'GestionExpedientes/editarCita.html'
    cita = get_object_or_404(Cita, pk=pk)

    if request.method == 'POST':
        form = NuevaCitaForm(request.POST, instance = cita)

        try:
            if form.is_valid():
                form.save()
                messages.success(request, "La cita fue modificada correctamente!")
                return redirect('gestionExp:listarCita')

        except Exception as e:
            messages.warning(request, 'Your Post Was Not Saved Due To An Error: {}'.format(e))
    else:
        form = NuevaCitaForm(instance=cita)

    context = {
        'form': form,
        'cita': cita
    }

    return render(request, template, context)


def cita_list(request):
    citas = Cita.objects.filter(fechaCita=timezone.now())
    return render(request,'GestionExpedientes/cita_dia.html', {'citas': citas})


def prueba(request):
 return render(request, 'GestionExpedientes/calendario_cita.html', {})
""" all_events = Cita.objects.all()
    event_arr = []

    for i in all_events:
        event_sub_arr = {}
        event_sub_arr['asuntoCita'] = i.asuntoCita
        event_sub_arr['fechaCita'] = i.fechaCita.strftime('%Y-%m-%d %H:%M:%S')
        event_arr.append(event_sub_arr)
    return HttpResponse(json.dumps(event_arr))


    context = {"events":all_events}
    return render(request,'GestionExpedientes/calendario_cita.html',context)"""

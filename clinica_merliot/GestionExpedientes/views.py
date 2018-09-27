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

from .forms import nuevoExpedienteForm, nuevoPacienteForm, ExpForm
from .models import Expediente, Paciente

from odontograma.models import Consulta
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

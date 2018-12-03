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

#Reportes
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from django.conf import settings
from io import BytesIO
from reportlab.pdfgen import canvas
from django.views.generic import View
from time import gmtime, strftime
import locale
from django.db import connection, connections
from .forms import *



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

 #Revisar las lineas de current_user y pdf.drawString(359, 727, current_user.username)
class ReportePacientesPDF(View):  

    showtime = strftime("%Y-%m-%d ", gmtime())
     
    def cabecera(self,request,pdf):
        #Utilizamos el archivo logo_django.png que está guardado en la carpeta media/imagenes
        archivo_imagen = 'static/images/logo.jpg'
        #Definimos el tamaño de la imagen a cargar y las coordenadas correspondientes
        pdf.drawImage(archivo_imagen, 40, 725, width=100, height=100) 
        showtime = strftime("%d-%m-%Y ", gmtime())
        current_user = request.user
        pdf.setFont("Times-Bold", 30)
        pdf.drawString(200, 787, u"Reporte Generado:")
        pdf.setFont("Helvetica", 20)
        pdf.drawString(210, 762, u"Reporte De Pacientes")
        pdf.setFont("Times-Bold", 11)
        pdf.drawString(150, 727, u"Fecha de emisión:")
        pdf.setFont("Times-Roman", 11)
        pdf.drawString(240, 727, showtime)
        pdf.setFont("Times-Bold", 11)  
        pdf.drawString(309, 727, u"Doctora:")
        pdf.setFont("Times-Roman", 11)
        pdf.drawString(359, 727, current_user.username)
        
        """pdf.setFont("Helvetica", 30)
        pdf.drawString(215, 790, u"Reporte GENERADO:")
        pdf.setFont("Helvetica", 20)
        pdf.drawString(260, 745, u"Reporte De Pacientes")""" 
        pdf.setTitle("Reporte de Pacientes Completo")  
        pdf.line(20,700,580,700)    

                 
    def get(self, request, *args, **kwargs):
        #Indicamos el tipo de contenido a devolver, en este caso un pdf
        response = HttpResponse(content_type='application/pdf')
        #La clase io.BytesIO permite tratar un array de bytes como un fichero binario, se utiliza como almacenamiento temporal
        buffer = BytesIO()
        #Canvas nos permite hacer el reporte con coordenadas X y Y
        pdf = canvas.Canvas(buffer)
        #Llamo al método cabecera donde están definidos los datos que aparecen en la cabecera del reporte.
        self.cabecera(request,pdf)
        y = 600
        self.tabla(pdf, y)
        #Con show page hacemos un corte de página para pasar a la siguiente
        pdf.showPage()
        pdf.save()
        pdf = buffer.getvalue()
        buffer.close()
        response.write(pdf)
        return response

    def tabla(self,pdf,y):
        #Creamos una tupla de encabezados para neustra tabla
        encabezados = ('Id', 'Nombre', 'Apellido', 'Sexo','Fecha Nacimiento')
        #Creamos una lista de tuplas que van a contener a las personas
        detalles = [(persona.id, persona.nombresPaciente, persona.apellidosPaciente, persona.sexo, persona.fechaNacimiento) for persona in Paciente.objects.all()]
        #Establecemos el tamaño de cada una de las columnas de la tabla
        detalle_orden = Table([encabezados] + detalles, colWidths=[2 * cm, 4 * cm, 4 * cm, 4 * cm])
        #Aplicamos estilos a las celdas de la tabla
        detalle_orden.setStyle(TableStyle(
            [
                #La primera fila(encabezados) va a estar centrada
                ('ALIGN',(0,0),(3,0),'CENTER'),
                #Los bordes de todas las celdas serán de color negro y con un grosor de 1
                ('GRID', (0, 0), (-1, -1), 1, colors.black), 
                #El tamaño de las letras de cada una de las celdas será de 10
                ('FONTSIZE', (0, 0), (-1, -1), 10),
            ]
        ))
        #Establecemos el tamaño de la hoja que ocupará la tabla 
        detalle_orden.wrapOn(pdf, 800, 600)
        #Definimos la coordenada donde se dibujará la tabla
        detalle_orden.drawOn(pdf, 40,y)

#------------------> Reporte General de Pacientes <------------------

def reporte1_crear(request):
    form1 = reportFecha()
    showtime = strftime("%d-%m-%Y ", gmtime())
    return render(request, 'GestionExpedientes/reporte1.html', {'form1':form1,'date':showtime})

class Reporte1(View):

    def get(self,request, *args, **kwargs):

        fech1 = self.kwargs['fecha']
        fech2 = self.kwargs['fecha2']
        response = HttpResponse(content_type='application/pdf')
        buffer = BytesIO()
        pdf = canvas.Canvas(buffer)
        self.cabecera(request,pdf)
        self.cuerpo(pdf,fech1,fech2)
       # self.tabla(pdf,fech1,fech2)
        self.pie(pdf)
        pdf.showPage()
        pdf.save()
        pdf = buffer.getvalue()
        buffer.close()
        response.write(pdf)
        return response  
     
    def cabecera(self,request,pdf):
       #Utilizamos el archivo logo_django.png que está guardado en la carpeta media/imagenes
        archivo_imagen = 'static/images/logo.jpg'
        #Definimos el tamaño de la imagen a cargar y las coordenadas correspondientes
        pdf.drawImage(archivo_imagen, 40, 725, width=100, height=100) 
        showtime = strftime("%d-%m-%Y ", gmtime())
        current_user = request.user
        pdf.setFont("Times-Bold", 30)
        pdf.drawString(200, 787, u"Reporte Generado:")
        pdf.setFont("Helvetica", 20)
        pdf.drawString(210, 762, u"Reporte De Pacientes")
        pdf.setFont("Times-Bold", 11)
        pdf.drawString(150, 727, u"Fecha de emisión:")
        pdf.setFont("Times-Roman", 11)
        pdf.drawString(240, 727, showtime)
        pdf.setFont("Times-Bold", 11)  
        pdf.drawString(309, 727, u"Doctora:")
        pdf.setFont("Times-Roman", 11)
        pdf.drawString(359, 727, current_user.username)
        
        """pdf.setFont("Helvetica", 30)
        pdf.drawString(215, 790, u"Reporte GENERADO:")
        pdf.setFont("Helvetica", 20)
        pdf.drawString(260, 745, u"Reporte De Pacientes")""" 
        pdf.setTitle("Reporte de Pacientes Atendidos")
        pdf.line(20,700,580,700)    


    def cuerpo(self,pdf,fech1,fech2):
    

        pdf.setFont("Times-Bold", 14)
        pdf.drawString(185, 650, "Reporte de Pacientes Atendidos en la Clinica")
        pdf.setFont("Times-Bold", 11)
        pdf.drawString(165, 600, "Fecha inicial:")
        pdf.setFont("Times-Roman", 11)
        pdf.drawString(240, 600, fech1)
        pdf.setFont("Times-Bold", 11)
        pdf.drawString(310, 600, "Fecha final:")
        pdf.setFont("Times-Roman", 11)
        pdf.drawString(375, 600, fech2)
        
       
    

    def pie(self,pdf):
        pdf.line(20,115,580,115)
        pdf.setFont("Helvetica", 12)
        pdf.drawString(200, 98, u"Clinica Dental Merliot")    
        pdf.drawString(190, 83, u"Universidad de El Salvador")
        pdf.drawString(130, 68, u"Final 25 Av. Nte, Ciudad Universitaria, San Salvador")
        pdf.drawString(200, 53, u"Tels.: (503) 2225 7198")
        pdf.drawString(182, 38, u"www.clinicaDental.com")
        archivo_imagen2 = 'static/images/logo2.jpg'
        pdf.drawImage(archivo_imagen2, 440 , 38, width=75, height=75)
        

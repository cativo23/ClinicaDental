from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Producto, Transaccion
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, TemplateView
from django.views.generic.edit import ModelFormMixin
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from django.shortcuts import get_object_or_404
from datetime import datetime
from .forms import nuevoProductoForm, existenciaProductoForm, editarProductoForm, existenciaProductoForm, nuevaTransacion

# Create your views here.


@login_required
def index(request):
    return render(request, 'GestionExpedientes/index.html', {})

class ProductoList(LoginRequiredMixin, ListView):
    model = Producto
    template_name = 'inventario/principalProducto.html'
    ordering = 'nombre_producto'

    def get_queryset(self):
        qs = Producto.objects.all()
        keywords = self.request.GET.get('q')
        if keywords:
            query = SearchQuery(keywords)
            vector = SearchVector('nombre_producto', 'marca_producto')
            qs = qs.annotate(search=vector).filter(search=query)
            qs = qs.annotate(rank=SearchRank(vector, query)).order_by('-rank')
        return qs


def ProductoListView(request):
    queryset_producto = Producto.objects.all()
    queryset_transaccion = Transaccion.objects.all()
    form_producto = nuevoProductoForm()
    form_transaccion = nuevaTransacion()
    context = {
        'object_list':queryset_producto,
        'form_producto':form_producto,
        'form_transaccion': form_transaccion,
        'transaccion_list':queryset_transaccion
    }

    if request.method == 'POST':
        if 'modalproducto' in request.POST:
            form_producto = nuevoProductoForm(request.POST)
            if form_producto.is_valid():
                form_producto.save()
            form_producto = nuevoProductoForm()

        if 'entrada' in request.POST:
            form_transaccion = nuevaTransacion(request.POST)
            if form_transaccion.is_valid():
                form_transaccion.save()
            form_transaccion = nuevaTransacion()

        if 'salida' in request.POST:
            form_transaccion = nuevaTransacion(request.POST)
            if form_transaccion.is_valid():
                form_transaccion.save()
            form_transaccion = nuevaTransacion()

        return render(request,'inventario/principalProducto.html' , context)


    return render(request,'inventario/principalProducto.html' , context)



@login_required
def agregarProducto(request):
    if request.method == 'POST':
        form = nuevoProductoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto guardado correctamente!')
            return redirect('inv:principalProducto')
    else:
        form = nuevoProductoForm()
    return render(request, 'inventario/agregarProducto.html', {'form': form, })

@login_required
def editarProducto(request, pk):
    template = 'inventario/editarProducto.html'
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        form = editarProductoForm(request.POST, instance=producto)
        try:
            if form.is_valid():
                form.save()
                messages.success(request, "El PRODUCTO FUE MODIFICADO CORRECTAMENTE!")
                return redirect('inv:principalProducto')
        except Exception as e:
            messages.warning(request, 'Your Post Was Not Saved Due To An Error: {}'.format(e))
    else:
        form = editarProductoForm(instance=producto)
    context = {
        'form': form,
        'producto': producto
    }
    return render(request, template, context)

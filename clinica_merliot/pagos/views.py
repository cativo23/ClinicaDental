from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import PagoForm
import GestionExpedientes
from django.contrib import messages
from django.shortcuts import render, redirect

# Create your views here.
@login_required
def agregarPago(request, id):
    template = 'pagos/agregarPago.html'

    expediente = GestionExpedientes.models.Expediente.objects.get(pk=id)
    if request.method == 'POST':
        form = PagoForm(request.POST)
        try:
            print(form)
            if form.is_valid():
                pago = form.save(commit=False)
                pago.expediente = expediente
                expediente.pagado += pago.cantidad
                expediente.saldo -= pago.cantidad
                pago.save()
                expediente.save()
                messages.success(request, "El pago Fue realizado correctamente!")
                return redirect('gestionExp:listarExpedientes')
        except Exception as e:
            print(e)
            messages.error(request, 'error: {}'.format(e))
    else:
        form = PagoForm()

    context = {
        'form': form
    }
    return render(request, template, context)

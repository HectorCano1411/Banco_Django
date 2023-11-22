# transferencias/views.py
from django.shortcuts import render, get_object_or_404, redirect
from .forms import TransferenciaForm
from .models import Transferencia
from iniciar.models import NuevoRegistro
from django.db.models import F
from datetime import datetime, timedelta
from decimal import Decimal
import json

def crear_transferencia(request):
    if request.method == 'POST':
        form = TransferenciaForm(request.POST)
        if form.is_valid():
            transferencia = form.save(commit=False)

            # Actualizar saldos de cuentas
            cuenta_origen = transferencia.cuenta_origen
            cuenta_destino = transferencia.cuenta_destino

            if cuenta_origen.SaldoContable >= transferencia.monto:
                cuenta_origen.SaldoContable = F('SaldoContable') - transferencia.monto
                cuenta_destino.SaldoContable = F('SaldoContable') + transferencia.monto

                # Convertir los campos Decimal a float antes de serializar a JSON
                transferencia.detalles = json.dumps({
                    'monto': float(transferencia.monto),
                    
                    # Agrega otros campos aquí...
                })

                transferencia.aprobada = True
                transferencia.save()

                cuenta_origen.save()
                cuenta_destino.save()

                # Puedes redirigir a una página de éxito o a cualquier otra vista después de guardar la transferencia
                return redirect('detalles_transferencia', transferencia.id)
            else:
                # Manejar el caso en que no hay saldo suficiente en la cuenta de origen
                form.add_error(None, 'Saldo insuficiente en la cuenta de origen.')
    else:
        form = TransferenciaForm()
        form.fields['cuenta_origen'].queryset = NuevoRegistro.objects.all()
        form.fields['cuenta_destino'].queryset = NuevoRegistro.objects.all()

    return render(request, 'transferencia_form.html', {'form': form})
# Otras vistas se mantienen similares, pero con ajustes para trabajar con el nuevo modelo de Cuenta y Transferencia.


# En detalles_transferencia, puedes obtener las cuentas asociadas a la transferencia:

def detalles_transferencia(request, transferencia_id):
    transferencia = get_object_or_404(Transferencia, pk=transferencia_id)

    # Recupera los detalles de la sesión
    detalles_transferencia = request.session.pop('detalles_transferencia', None)

    if detalles_transferencia:
        # Agrega los detalles a la transferencia
        transferencia.monto = detalles_transferencia['monto']
        transferencia.descripcion = detalles_transferencia['descripcion']
        # Ajusta según sea necesario para otros detalles

    cuenta_origen = transferencia.cuenta_origen
    cuenta_destino = transferencia.cuenta_destino

    return render(request, 'detalles_transferencia.html', {'transferencia': transferencia, 'cuenta_origen': cuenta_origen, 'cuenta_destino': cuenta_destino})

# Las demás vistas se pueden ajustar de manera similar, considerando el nuevo modelo Cuenta y la relación con NuevoRegistro.


# Por ejemplo, en listar_transferencias, se puede hacer:
def listar_transferencias(request):
    transferencias = Transferencia.objects.all()
    return render(request, 'listar_transferencias.html', {'transferencias': transferencias})
# Las demás vistas se pueden ajustar de manera similar, considerando el nuevo modelo Cuenta y la relación con NuevoRegistro.

def aprobar_transferencia(request, transferencia_id):
    transferencia = get_object_or_404(Transferencia, pk=transferencia_id)

    # Lógica para aprobar la transferencia
    if not transferencia.aprobada:
        # Actualizar saldos de cuentas
        cuenta_origen = transferencia.cuenta_origen
        cuenta_destino = transferencia.cuenta_destino

        cuenta_origen.SaldoContable = F('SaldoContable') - transferencia.monto
        cuenta_destino.SaldoContable = F('SaldoContable') + transferencia.monto

        transferencia.aprobada = True

        cuenta_origen.save()
        cuenta_destino.save()
        transferencia.save()

    return render(request, 'aprobar_transferencia.html', {'transferencia': transferencia})

def informe_transferencias(request, transferencia_id):
    transferencias = get_object_or_404(Transferencia, pk=transferencia_id)

    # Lógica para generar el informe (puedes utilizar bibliotecas como pandas para análisis de datos)
    transferencias = Transferencia.objects.all()
    return render(request, 'informe_transferencias.html', {'transferencias': transferencias})

def cancelar_transferencia(request, transferencia_id):
    transferencia = get_object_or_404(Transferencia, pk=transferencia_id)

    # Lógica para cancelar la transferencia
    if not transferencia.aprobada:
        # Actualizar saldo de cuenta de origen
        cuenta_origen = transferencia.cuenta_origen
        cuenta_origen.SaldoContable = F('SaldoContable') + transferencia.monto
        cuenta_origen.save()

        transferencia.delete()

    return render(request, 'cancelar_transferencia.html', {'transferencia': transferencia})

def historial_saldo(request, transferencia_id):
    transferencia = get_object_or_404(Transferencia, pk=transferencia_id)
    transferencias = Transferencia.objects.all()
    # Obtén la fecha actual
    fecha_actual = datetime.now()

    # Define el rango de fechas para el historial (por ejemplo, últimos 30 días)
    fecha_inicio = fecha_actual - timedelta(days=30)

    # Filtra las transferencias en el rango de fechas
    historial = Transferencia.objects.filter(fecha__range=(fecha_inicio, fecha_actual)).order_by('-fecha')

    return render(request, 'historial_saldo.html', {'historial': historial})
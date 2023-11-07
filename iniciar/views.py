import re
from decimal import Decimal

from django.urls import reverse
from .models import NuevoRegistro
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password ,check_password
from django.shortcuts import render, redirect
from django.contrib import messages 
from django.db import IntegrityError
from .forms import RegistroNuevoForm
from datetime import datetime
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from decimal import Decimal
from django.db import transaction




def handle_errors(view_func):
    def wrapped_view(request, *args, **kwargs):
        try:
            return view_func(request, *args, **kwargs)
        except IntegrityError as e:
            # Manejo de errores de integridad de la base de datos
            error_message = str(e)
            return render(request, 'error.html', {'error_message': error_message})
        except NuevoRegistro.DoesNotExist:
            # Manejo de errores para usuario no encontrado
            error_message = 'Usuario no encontrado'
            return render(request, 'error.html', {'error_message': error_message})
        except Exception as e:
            # Manejo de otros errores no capturados, como errores personalizados
            error_message = str(e)
            return render(request, 'error.html', {'error_message': error_message})

    return wrapped_view

def registro_usuario(request):
    if request.method == 'POST':
        form = RegistroNuevoForm(request.POST)
        if form.is_valid():
            usuario = form.save(commit=False)  # Guarda el usuario sin commit
            clave = form.cleaned_data['clave1']  # Obtiene la contraseña encriptada
            usuario.Clave = make_password(clave)

            try:
                usuario.save()  # Intenta guardar el usuario en la base de datos
                print('Clave guardada exitosamente en la base de datos')
                messages.success(request, 'Registro exitoso. Ahora puedes iniciar sesión.')
                return redirect('custom_login')  # Redirige al detalle de la cuenta
            except Exception as e:
                print(f'Error al guardar la clave en la base de datos: {e}')
                messages.error(request, 'Hubo un error al guardar la clave. Por favor, inténtalo de nuevo.')

        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = RegistroNuevoForm()
    return render(request, 'registro_usuario.html', {'form': form})


# def custom_login(request):
#     if request.method == 'POST':
#         rut = request.POST.get('rut')
#         clave = request.POST.get('clave')
#         try:
#             usuario = NuevoRegistro.objects.get(rut=rut)
#             if not usuario.Estado:
#                 messages.warning(request, 'Tu cuenta está bloqueada. Contacta al soporte.')
#                 return render(request, 'login.html')
#             if check_password(clave, usuario.Clave):
#                 usuario.intentos_fallidos = 0  # Reiniciar intentos fallidos
#                 usuario.save()
#                 return redirect('detalle_cuenta', usuario_id=usuario.id)
#             usuario.intentos_fallidos += 1
#             if usuario.intentos_fallidos == 1:
#                 messages.warning(request, 'Primer intento fallido.')
#             elif usuario.intentos_fallidos == 2:
#                 messages.warning(request, 'Segundo intento fallido. Le queda un intento.')
#             elif usuario.intentos_fallidos >= 3:
#                 usuario.Estado = False
#                 usuario.save()
#                 messages.error(request, 'Tu cuenta ha sido bloqueada. Por favor, contacta al soporte.')
                
#             usuario.save()  # Guardar cambios en los intentos fallidos
#         except NuevoRegistro.DoesNotExist:
#             messages.error(request, 'Usuario no encontrado')

#     return render(request, 'login.html')


def custom_login(request):
    if request.method == 'POST':
        rut = request.POST.get('rut')
        clave = request.POST.get('clave')
        try:
            usuario = NuevoRegistro.objects.get(rut=rut)
            if not usuario.Estado:
                messages.warning(request, 'Tu cuenta está bloqueada. Contacta al soporte.')
                return render(request, 'login.html')
            if check_password(clave, usuario.Clave):
                usuario.intentos_fallidos = 0  # Reiniciar intentos fallidos
                usuario.save()

                # Almacena el RUT del usuario autenticado en la sesión
                request.session['rut'] = rut

                return redirect('detalle_cuenta', usuario_id=usuario.id)
            usuario.intentos_fallidos += 1
            if usuario.intentos_fallidos == 1:
                messages.warning(request, 'Primer intento fallido.')
            elif usuario.intentos_fallidos == 2:
                messages.warning(request, 'Segundo intento fallido. Le queda un intento.')
            elif usuario.intentos_fallidos >= 3:
                usuario.Estado = False
                usuario.save()
                messages.error(request, 'Tu cuenta ha sido bloqueada. Por favor, contacta al soporte.')

            usuario.save()  # Guardar cambios en los intentos fallidos
        except NuevoRegistro.DoesNotExist:
            messages.error(request, 'Usuario no encontrado')

    return render(request, 'login.html')

# @transaction.atomic
# @login_required
# def ingresar_valor(request, usuario_id):
#     try:
#         usuario = NuevoRegistro.objects.get(id=usuario_id)

#         if request.method == 'POST':
#             nombre = request.POST.get('nombre')
#             rut = request.POST.get('rut')
#             monto_str = request.POST.get('monto', '0')

#             if not monto_str.isdigit():
#                 messages.error(request, 'Solo se pueden ingresar valores enteros.')
#             else:
#                 monto = Decimal(monto_str)  # Convertir el valor a Decimal

#                 if monto <= Decimal('0'):
#                     messages.error(request, 'El monto debe ser mayor que cero.')
#                 else:
#                     if usuario.SaldoCuentaCorriente is None:
#                         usuario.SaldoCuentaCorriente = Decimal('0.0')

#                     # Realizar la operación de ingreso de valor y actualizar el saldo
#                     usuario.SaldoCuentaCorriente += monto
#                     usuario.save()
#                     messages.success(request, f'Se ingresó ${monto} a la cuenta de {nombre} (RUT: {rut}) exitosamente.')

#                     # Aquí convierte el objeto Decimal a un número de punto flotante
#                     monto_float = float(monto)

#                     # Guarda los datos necesarios en la sesión para la vista de comprobante
#                     request.session['nombre'] = nombre
#                     request.session['rut'] = rut
#                     request.session['monto'] = monto_float

#                     # Redirecciona a la vista 'comprobante'
#                     return redirect('comprobante', usuario_id=usuario_id)

#     except NuevoRegistro.DoesNotExist:
#         return JsonResponse({'error': 'Usuario no encontrado'}, status=404)

#     return render(request, 'ingresar_valor.html', {'usuario': usuario})
# @transaction.atomic
# @login_required
# def ingresar_valor(request, usuario_id):
#     try:
#         usuario = NuevoRegistro.objects.get(id=usuario_id)

#         if request.method == 'POST':
#             nombre = request.POST.get('nombre')
#             rut_ingresado = request.POST.get('rut')
#             monto_str = request.POST.get('monto', '0')

#             # Obtener el RUT del usuario autenticado desde la sesión
#             rut_autenticado = request.session.get('rut')

#             # Verificar que el RUT almacenado en la sesión coincida con el RUT ingresado
#             if rut_autenticado != rut_ingresado:
#                 messages.error(request, 'El RUT ingresado no coincide con tu RUT.')
#                 return render(request, 'ingresar_valor.html', {'usuario': usuario})

#             # Validar que el monto sea un valor entero
#             if not monto_str.isdigit():
#                 messages.error(request, 'Solo se pueden ingresar valores enteros mayores a 0.')
#                 return render(request, 'ingresar_valor.html', {'usuario': usuario})

#             monto = Decimal(monto_str)  # Convertir el valor a Decimal

#             if monto <= Decimal('0'):
#                 messages.error(request, 'El monto debe ser mayor que cero.')
#             else:
#                 if usuario.SaldoCuentaCorriente is None:
#                     usuario.SaldoCuentaCorriente = Decimal('0.0')

#                 # Realizar la operación de ingreso de valor y actualizar el saldo
#                 usuario.SaldoCuentaCorriente += monto
#                 usuario.SaldoContable = usuario.SaldoCuentaCorriente - usuario.TotalCargos + usuario.TotalAbonos
#                 usuario.SaldoLineaCredito = usuario.SaldoCuentaCorriente
#                 usuario.save()
#                 messages.success(request, f'Se ingresó ${monto} a la cuenta de {nombre} (RUT: {rut_ingresado}) exitosamente.')

#                 # Aquí convierte el objeto Decimal a un número de punto flotante
#                 monto_float = float(monto)

#                 # Guarda los datos necesarios en la sesión para la vista de comprobante
#                 request.session['nombre'] = nombre
#                 request.session['rut'] = rut_ingresado
#                 request.session['monto'] = monto_float

#                 # Redirecciona a la vista 'comprobante'
#                 return redirect('comprobante', usuario_id=usuario_id)

#     except NuevoRegistro.DoesNotExist:
#         return JsonResponse({'error': 'Usuario no encontrado'}, status=404)

#     return render(request, 'ingresar_valor.html', {'usuario': usuariofrom decimal import Decimal


def ingresar_valor(request, usuario_id):
    try:
        usuario = NuevoRegistro.objects.get(id=usuario_id)

        if request.method == 'POST':
            nombre = request.POST.get('nombre')
            rut_ingresado = request.POST.get('rut')
            monto_str = request.POST.get('monto', '0')
            # Verificar que el nombre solo contenga letras
            if not re.match("^[A-Za-z\s]*$", nombre):
                messages.error(request, 'El nombre solo debe contener letras y espacios.')
                return render(request, 'ingresar_valor.html', {'usuario': usuario})

            # Obtener el RUT del usuario autenticado desde la sesión
            rut_autenticado = request.session.get('rut')

            # Verificar que el RUT almacenado en la sesión coincida con el RUT ingresado
            if rut_autenticado != rut_ingresado:
                messages.error(request, 'El RUT ingresado no coincide con tu RUT del Titular.')
                return render(request, 'ingresar_valor.html', {'usuario': usuario})

            # Validar que el monto sea un valor entero
            if not monto_str.isdigit():
                messages.error(request, 'Solo se pueden ingresar valores enteros mayores a 0.')
                return render(request, 'ingresar_valor.html', {'usuario': usuario})

            monto = Decimal(monto_str)  # Convertir el valor a Decimal

            if monto <= Decimal('0'):
                messages.error(request, 'El monto debe ser mayor que cero.')
            else:
                if usuario.SaldoCuentaCorriente is None:
                    usuario.SaldoCuentaCorriente = Decimal('0.0')

                # Realizar la operación de ingreso de valor y actualizar el saldo
                if usuario.SaldoCuentaCorriente is not None:
                    usuario.SaldoCuentaCorriente += monto
                else:
                    usuario.SaldoCuentaCorriente = monto

                usuario.save()
                messages.success(request, f'Se ingresó ${monto} a la cuenta de {nombre} (RUT: {rut_ingresado}) exitosamente.')

                # Actualizar SaldoContable y SaldoLineaCredito en la vista detalle_cuenta
                if usuario.SaldoCuentaCorriente is not None:
                    usuario.SaldoContable = usuario.SaldoCuentaCorriente
                    usuario.SaldoLineaCredito = usuario.SaldoCuentaCorriente * Decimal('0.8')  # Ejemplo de cálculo
                    usuario.save()

                # Actualizar TotalCargos y TotalAbonos
                # if usuario.TotalCargos is not None:
                #     usuario.TotalCargos += monto
                # else:
                #     usuario.TotalCargos = monto

                if usuario.TotalAbonos is not None:
                    usuario.TotalAbonos += monto
                else:
                    usuario.TotalAbonos = monto

                usuario.save()

                # Aquí convierte el objeto Decimal a un número de punto flotante
                monto_float = float(monto)

                # Guarda los datos necesarios en la sesión para la vista de comprobante
                request.session['nombre'] = nombre
                request.session['rut'] = rut_ingresado
                request.session['monto'] = monto_float

                # Redirecciona a la vista 'comprobante'
                return redirect('comprobante', usuario_id=usuario_id)

    except NuevoRegistro.DoesNotExist:
        messages.error(request, 'El usuario no existe.')

    return render(request, 'ingresar_valor.html', {'usuario': usuario})





# @transaction.atomic
# @login_required
# def realizar_retiro(request, usuario_id):
#     try:
#         usuario = NuevoRegistro.objects.get(id=usuario_id)
#     except NuevoRegistro.DoesNotExist:
#         messages.error(request, 'Usuario no encontrado')
#         return redirect('detalle_cuenta', usuario_id=usuario_id)

#     if request.method == 'POST':
#         monto = request.POST.get('monto', '0.0')  # Obtener el monto como cadena

#         if not monto.isdigit():
#             messages.error(request, 'Solo se pueden retirar valores enteros y el monto debe ser mayor a 0.')
#             return redirect('realizar_retiro', usuario_id=usuario_id)

#         monto_decimal = Decimal(monto)  # Convertir la cadena a Decimal

#         if monto_decimal <= Decimal('0.0'):
#             messages.error(request, 'El monto a retirar debe ser mayor que cero.')
#         elif monto_decimal > usuario.SaldoCuentaCorriente:
#             messages.error(request, 'No tienes suficientes fondos para realizar este retiro.')
#         else:
#             # Realizar la operación de retiro de valor y actualizar el saldo
#             usuario.SaldoCuentaCorriente -= monto_decimal
#             usuario.save()
#             messages.success(request, f'Se retiró ${monto_decimal} de la cuenta exitosamente.')

#             # Datos a enviar a la vista de comprobante
#             nombre = usuario.Nombres
#             rut = usuario.rut

#             # Guarda los datos necesarios en la sesión para la vista de comprobante
#             request.session['nombre'] = nombre
#             request.session['rut'] = rut
#             request.session['monto'] = float(monto_decimal)  # Convierte el Decimal a float

#             return redirect('comprobante_retiro', usuario_id=usuario_id)

#     return render(request, 'realizar_retiro.html', {'usuario': usuario})
from decimal import Decimal
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import transaction
from .models import NuevoRegistro

@transaction.atomic
@login_required
def realizar_retiro(request, usuario_id):
    try:
        usuario = NuevoRegistro.objects.get(id=usuario_id)
    except NuevoRegistro.DoesNotExist:
        messages.error(request, 'Usuario no encontrado')
        return redirect('detalle_cuenta', usuario_id=usuario_id)

    if request.method == 'POST':
        monto = request.POST.get('monto', '0.0')  # Obtener el monto como cadena

        if not monto.isdigit():
            messages.error(request, 'Solo se pueden retirar valores enteros y el monto debe ser mayor a 0.')
            return redirect('realizar_retiro', usuario_id=usuario_id)

        monto_decimal = Decimal(monto)  # Convertir la cadena a Decimal

        if monto_decimal <= Decimal('0.0'):
            messages.error(request, 'El monto a retirar debe ser mayor que cero.')
        elif monto_decimal > usuario.SaldoCuentaCorriente:
            messages.error(request, 'No tienes suficientes fondos para realizar este retiro.')
        else:
            with transaction.atomic():
                # Realizar la operación de retiro de valor y actualizar el saldo
                usuario.SaldoCuentaCorriente -= monto_decimal

                # Actualizar TotalCargos con el monto del retiro
                if usuario.TotalCargos is not None:
                    usuario.TotalCargos -= monto_decimal
                else:
                    usuario.TotalCargos = monto_decimal

                usuario.save()
                messages.success(request, f'Se retiró ${monto_decimal} de la cuenta exitosamente.')

                # Datos a enviar a la vista de comprobante
                nombre = usuario.Nombres
                rut = usuario.rut

                # Guarda los datos necesarios en la sesión para la vista de comprobante
                request.session['nombre'] = nombre
                request.session['rut'] = rut
                request.session['monto'] = float(monto_decimal)  # Convierte el Decimal a float

                return redirect('comprobante_retiro', usuario_id=usuario_id)

    return render(request, 'realizar_retiro.html', {'usuario': usuario})


def comprobante(request, usuario_id):
    try:
        usuario = NuevoRegistro.objects.get(id=usuario_id)

        # Obtiene los datos de la transacción del último mensaje en la sesión
        nombre = request.session.get('nombre')
        rut = request.session.get('rut')
        monto = request.session.get('monto')

        # Ajusta los campos según tu modelo
        # Por ejemplo, puedes agregar otros campos como 'NumeroCuenta', 'SaldoCuentaCorriente', etc.
        detalle_cuenta_url = reverse('detalle_cuenta', args=[usuario_id])
        
        


        return render(request, 'comprobante.html', {
            'detalle_cuenta_url': detalle_cuenta_url,
            'usuario': usuario,
            'nombre': nombre,
            'rut': rut,
            'monto': monto,
        })

    except NuevoRegistro.DoesNotExist:
        raise Http404("Usuario no encontrado")


def comprobante_retiro(request, usuario_id):
    usuario = get_object_or_404(NuevoRegistro, id=usuario_id)

    nombre = request.session.get('nombre')
    rut = request.session.get('rut')
    monto = request.session.get('monto')
    detalle_cuenta_url = reverse('detalle_cuenta', args=[usuario_id])


    return render(request, 'comprobante_retiro.html', {
        'detalle_cuenta_url': detalle_cuenta_url,
        'usuario': usuario,
        'nombre': nombre,
        'rut': rut,
        'monto': monto,
    })


@handle_errors
def detalle_cuenta(request, usuario_id):
    try:
        usuario = NuevoRegistro.objects.get(id=usuario_id)        
        now = datetime.now()
        context = {
            'usuario': usuario,
            'fecha_actual': now,
        }
        return render(request, 'detalle_cuenta.html', context)
    except NuevoRegistro.DoesNotExist:
        messages.error(request, 'Usuario no encontrado')
    
    return redirect('custom_login')


def lista_usuarios(request):
    usuarios = NuevoRegistro.objects.all()
    return render(request, 'lista_usuarios.html', {'usuarios': usuarios})

def bloquear_usuario(request, usuario_id):
    usuario = get_object_or_404(NuevoRegistro, pk=usuario_id)
    usuario.Estado = not usuario.Estado
    usuario.save()
    return redirect('lista_usuarios')

# from django.http import FileResponse
# from django.shortcuts import get_object_or_404
# from django.http import Http404
# from .models import NuevoRegistro

# def descargar_comprobante(request, usuario_id):
#     try:
#         # Obtén el objeto NuevoRegistro correspondiente al usuario
#         usuario = get_object_or_404(NuevoRegistro, id=usuario_id)

#         # Aquí es donde debes generar o recuperar el comprobante. Supongamos que generas un PDF con ReportLab.
#         from reportlab.lib.pagesizes import letter
#         from reportlab.lib import colors
#         from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
#         from reportlab.platypus.tables import Table
#         from reportlab.platypus.styles import getSampleStyleSheet
#         from io import BytesIO

#         buffer = BytesIO()
#         pdf = SimpleDocTemplate(buffer, pagesize=letter)
#         pdf_title = "Comprobante de Ingreso"
#         styles = getSampleStyleSheet()
#         story = []

#         # Agregar el contenido del comprobante, personaliza esto según tus necesidades.
#         story.append(Paragraph(f'<strong>Nombre:</strong> {usuario.Nombres}', styles["Normal"]))
#         story.append(Spacer(1, 12))
#         story.append(Paragraph(f'<strong>RUT:</strong> {usuario.rut}', styles["Normal"]))
#         story.append(Spacer(1, 12))
#         story.append(Paragraph(f'<strong>Monto:</strong> {usuario.SaldoCuentaCorriente}', styles["Normal"]))

#         # Agrega más contenido si es necesario, como el número de cuenta, fecha, etc.

#         # Construir el PDF
#         pdf.build(story)
#         buffer.seek(0)

#         # Preparar una respuesta para descargar el PDF
#         response = FileResponse(buffer, content_type='application/pdf')
#         response['Content-Disposition'] = f'attachment; filename="comprobante.pdf"'
#         return response

#     except NuevoRegistro.DoesNotExist:
#         raise Http404("Usuario no encontrado")

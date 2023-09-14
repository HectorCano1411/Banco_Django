from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password ,check_password
from django.shortcuts import render, redirect
from django.contrib import messages 
from django.db import IntegrityError
from .forms import RegistroNuevoForm
from .models import NuevoRegistro
from datetime import datetime

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


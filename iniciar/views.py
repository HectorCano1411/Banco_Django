

from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from django.db import IntegrityError
from .models import Usuario
from .models import SecurityAudit


def handle_errors(view_func):
    def wrapped_view(request, *args, **kwargs):
        try:
            return view_func(request, *args, **kwargs)
        except IntegrityError as e:
            # Manejo de errores de integridad de la base de datos
            error_message = str(e)
            return render(request, 'error.html', {'error_message': error_message})
        except Usuario.DoesNotExist:
            # Manejo de errores para usuario no encontrado
            error_message = 'Usuario no encontrado'
            return render(request, 'error.html', {'error_message': error_message})
        except Exception as e:
            # Manejo de otros errores no capturados, como errores personalizados
            error_message = str(e)
            return render(request, 'error.html', {'error_message': error_message})

    return wrapped_view

@handle_errors
def custom_login(request):
    if request.method == 'POST':
        rut = request.POST.get('rut')
        clave = request.POST.get('clave')
        
        try:
            usuario = Usuario.objects.get(Rut=rut)
            
            # Verificar el estado de la cuenta
            if not usuario.Estado:
                messages.warning(request, 'Tu cuenta está bloqueada. Contacta al soporte.')
                return redirect('login.html')  # Cambia 'pagina_principal' al nombre de tu página principal

            if usuario.Clave == clave:
                usuario.intentos_fallidos = 0  # Reiniciar intentos fallidos
                usuario.save()

                # Registrar evento de inicio de sesión exitoso en el registro de auditoría
                SecurityAudit.objects.create(
                    user=usuario,
                    event_type='Inicio de sesión exitoso',
                    details='El usuario ha iniciado sesión correctamente.'
                )

                return redirect('detalle_cuenta', usuario_id=usuario.id)
            
            usuario.intentos_fallidos += 1
            if usuario.intentos_fallidos == 1:
                messages.warning(request, 'Primer intento fallido.')
            elif usuario.intentos_fallidos == 2:
                messages.warning(request, 'Segundo intento fallido. Le queda un intento.')
            elif usuario.intentos_fallidos >= 3:
                usuario.Estado = False
                usuario.save()

                # Registrar evento de bloqueo de cuenta en el registro de auditoría
                SecurityAudit.objects.create(
                    user=usuario,
                    event_type='Cuenta bloqueada',
                    details='La cuenta del usuario se ha bloqueado debido a intentos fallidos de inicio de sesión.'
                )

                messages.error(request, 'Tu cuenta ha sido bloqueada. Por favor, contacta al soporte.')
                return redirect('custom_login')
                
            usuario.save()  # Guardar cambios en los intentos fallidos
        except Usuario.DoesNotExist:
            messages.error(request, 'Usuario no encontrado')

    return render(request, 'login.html')

@   handle_errors
def detalle_cuenta(request, usuario_id):
    try:
        usuario = Usuario.objects.get(id=usuario_id)
        
        now = datetime.now()

        # Agregar la fecha y hora actual al contexto junto con el usuario
        context = {
            'usuario': usuario,
            'fecha_actual': now,
        }

        return render(request, 'detalle_cuenta.html', context)
    except Usuario.DoesNotExist:
        messages.error(request, 'Usuario no encontrado')
    
    return redirect('custom_login')


@login_required  # Asegura que solo los administradores autenticados puedan acceder a esta vista
def desbloquear_cuenta(request, usuario_id):
    try:
        usuario = Usuario.objects.get(id=usuario_id)
        
        # Verificar si la cuenta está bloqueada
        if not usuario.Estado:
            if request.method == 'POST':
                # Asegurarse de que el formulario fue enviado y confirmar desbloqueo
                usuario.Estado = True  # Desbloquear la cuenta
                usuario.intentos_fallidos = 0  # Reiniciar intentos fallidos
                usuario.save()
                messages.success(request, f'La cuenta de {usuario.Nombres} {usuario.Apellidos} ha sido desbloqueada.')
                return redirect('custom_login') 
               
                return render(request, 'desbloquear_cuenta.html', {'usuario': usuario})
        else:
            messages.warning(request, 'La cuenta ya está desbloqueada.')
            return redirect('custom_login')  
    except Usuario.DoesNotExist:
        messages.error(request, 'Usuario no encontrado')
        return redirect('custom_login') 
from django.contrib import admin
from .models import Usuario
from .models import SecurityAudit  
from .models import NuevoRegistro  # Asegúrate de importar el modelo NuevoRegistro desde tu aplicación

# Register your models here.




class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('Rut', 'Nombres', 'Apellidos', 'Estado')
    list_filter = ('Estado',)
        
admin.site.register(Usuario, UsuarioAdmin)


class SecurityAuditAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'user', 'event_type')
    list_filter = ('event_type', 'user')
    search_fields = ('user__username', 'event_type')
    readonly_fields = ('timestamp', 'user', 'event_type', 'details')

admin.site.register(SecurityAudit, SecurityAuditAdmin)



# Define una clase personalizada para la administración de NuevoRegistro
class NuevoRegistroAdmin(admin.ModelAdmin):
    list_display = ('rut', 'Nombres', 'Apellidos', 'Estado')  # Cambia "Rut" a "rut"
    list_filter = ('Estado',)  
    search_fields = ('rut', 'Nombres', 'Apellidos') 

admin.site.register(NuevoRegistro, NuevoRegistroAdmin)

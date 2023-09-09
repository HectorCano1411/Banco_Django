from django.contrib import admin
from .models import Usuario
from .models import SecurityAudit  
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
# transferencias/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('crear_transferencia/', views.crear_transferencia, name='crear_transferencia'),
    path('listar_transferencias/<int:transferencia_id>/', views.listar_transferencias, name='listar_transferencias'),
    path('detalles_transferencia/<int:transferencia_id>/', views.detalles_transferencia, name='detalles_transferencia'),
    path('aprobar_transferencia/<int:transferencia_id>/', views.aprobar_transferencia, name='aprobar_transferencia'),
    path('informe_transferencias/<int:transferencia_id>/', views.informe_transferencias, name='informe_transferencias'),
    path('cancelar_transferencia/<int:transferencia_id>/', views.cancelar_transferencia, name='cancelar_transferencia'),
    path('historial_saldo/<int:transferencia_id>/', views.historial_saldo, name='historial_saldo'),
]

from django.contrib import admin
from django.urls import path
from iniciar import views


urlpatterns = [
    path('registro/', views.registro_usuario, name='registro_usuario'),
    path('detalle_cuenta/<int:usuario_id>/', views.detalle_cuenta, name='detalle_cuenta'),  
    path('desbloquear/<int:usuario_id>/', views.desbloquear_cuenta, name='desbloquear_cuenta'),    
]
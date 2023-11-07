from django.contrib import admin
from django.urls import path
from iniciar import views


urlpatterns = [
    path('registro/', views.registro_usuario, name='registro_usuario'),
    path('detalle_cuenta/<int:usuario_id>/', views.detalle_cuenta, name='detalle_cuenta'),  
    path('ingresar_valor/<int:usuario_id>/', views.ingresar_valor, name='ingresar_valor'),
    path('realizar_retiro/<int:usuario_id>/', views.realizar_retiro, name='realizar_retiro'),
    path('comprobante/<int:usuario_id>/', views.comprobante, name='comprobante'),
    path('comprobante_retiro/<int:usuario_id>/', views.comprobante_retiro, name='comprobante_retiro'),
    path('bloquear_usuario/<int:usuario_id>/', views.bloquear_usuario, name='bloquear_usuario'),
    path('lista_usuarios/', views.lista_usuarios, name='lista_usuarios'),
    path('bloquear_usuario/<int:usuario_id>/', views.bloquear_usuario, name='bloquear_usuario'),
]
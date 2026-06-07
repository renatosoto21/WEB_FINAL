from django.urls import path
from . import views

urlpatterns = [
    path('perfil/', views.perfil, name='perfil'),
    path('iniciar-sesion/', views.iniciar_sesion, name='login'),
    path('registrarse/', views.registrarse, name='registrarse'),
    path('cerrar-sesion/', views.cerrar_sesion, name='logout'),
    path('editar-perfil/', views.editar_perfil, name='editar_perfil'),
]
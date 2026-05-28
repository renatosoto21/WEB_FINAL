from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('mas_ventas/', views.mas_ventas, name='mas_ventas'),
    path('nuevos_lanzamientos/', views.nuevos_lanzamientos, name='nuevos_lanzamientos'),
    path('admin-panel/', views.panel_admin, name='panel_admin'),
    path('admin-panel/nuevo/', views.crear_juego, name='crear_juego'),
    path('admin-panel/', views.panel_admin, name='panel_admin'),
    path('admin-panel/nuevo/', views.crear_juego, name='crear_juego'),
    path('admin-panel/editar/<int:pk>/', views.editar_juego, name='editar_juego'),
    path('admin-panel/eliminar/<int:pk>/', views.eliminar_juego, name='eliminar_juego'),
    path('admin-panel/agregar/', views.agregar_juego, name='agregar_juego'),
    path('eliminar-usuario/<int:user_id>/', views.eliminar_usuario, name='eliminar_usuario'),
]
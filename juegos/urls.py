from django.urls import path
from . import views

urlpatterns = [
    # Frontend - Vistas públicas
    path('', views.index, name='index'),
    path('mas_ventas/', views.mas_ventas, name='mas_ventas'),
    path('nuevos_lanzamientos/', views.nuevos_lanzamientos, name='nuevos_lanzamientos'),
    path('categorias/', views.listar_categorias, name='listar_categorias'),
    path('categoria/<slug:slug>/', views.ver_categoria, name='ver_categoria'),

    # Autenticación
    path('iniciar-sesion/', views.iniciar_sesion, name='login'),
    path('cerrar-sesion/', views.cerrar_sesion, name='logout'),

    # Admin Panel - Videojuegos
    path('admin-panel/', views.panel_admin, name='panel_admin'),
    path('admin-panel/nuevo/', views.crear_juego, name='crear_juego'),
    path('admin-panel/agregar/', views.agregar_juego, name='agregar_juego'),
    path('admin-panel/editar/<int:pk>/', views.editar_juego, name='editar_juego'),
    path('admin-panel/eliminar/<int:pk>/', views.eliminar_juego, name='eliminar_juego'),

    # Admin Panel - Categorías
    path('admin-panel/categorias/', views.admin_categorias, name='admin_categorias'),
    path('admin-panel/categorias/nueva/', views.admin_agregar_categoria, name='admin_agregar_categoria'),
    path('admin-panel/categorias/editar/<int:pk>/', views.admin_editar_categoria, name='admin_editar_categoria'),
    path('admin-panel/categorias/eliminar/<int:pk>/', views.admin_eliminar_categoria, name='admin_eliminar_categoria'),
]

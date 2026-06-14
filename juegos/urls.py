from django.urls import path
from . import views

urlpatterns = [
    # Frontend - Vistas públicas
    path('', views.index, name='index'),
    path('mas_ventas/', views.mas_ventas, name='mas_ventas'),
    path('nuevos_lanzamientos/', views.nuevos_lanzamientos, name='nuevos_lanzamientos'),
    path('categorias/', views.listar_categorias, name='listar_categorias'),
    path('categoria/<slug:slug>/', views.ver_categoria, name='ver_categoria'),
    path('mis_favoritos/', views.ver_favoritos, name='ver_favoritos'),
    path('agregar_favoritos/<int:juego_id>/', views.agregar_favorito, name='agregar_favoritos'),
    path('nuestro_catalogo/', views.nuestro_catalogo, name='nuestro_catalogo'),

    # Autenticación
    path('iniciar-sesion/', views.iniciar_sesion, name='login'),
    path('cerrar-sesion/', views.cerrar_sesion, name='logout'),

    # Admin Panel - Videojuegos
    path('admin-panel/', views.panel_admin, name='panel_admin'),
    path('admin-panel/nuevo/', views.crear_juego, name='crear_juego'),
    path('admin-panel/agregar/', views.agregar_juego, name='agregar_juego'),
    path('admin-panel/editar/<int:pk>/', views.editar_juego, name='editar_juego'),
    path('admin-panel/eliminar/<int:pk>/', views.eliminar_juego, name='eliminar_juego'),

    # Admin Panel - Usuarios
    path('panel-admin/eliminar-usuario/<int:user_id>/', views.eliminar_usuario, name='eliminar_usuario'),

    # Admin Panel - Categorías
    path('admin-panel/categorias/', views.admin_categorias, name='admin_categorias'),
    path('panel-admin/crear-categoria/', views.crear_categoria, name='crear_categoria'),
    path('panel-admin/editar-categoria/<int:cat_id>/', views.editar_categoria, name='editar_categoria'),
    path('panel-admin/eliminar-categoria/<int:cat_id>/', views.eliminar_categoria, name='eliminar_categoria'),
]

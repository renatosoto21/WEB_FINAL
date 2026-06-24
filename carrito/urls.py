from django.urls import path
from . import views


urlpatterns = [
    # Rutas de pago 
    path('compra/', views.compra, name='compra'),
    path('pagar/', views.procesar_pago, name='pagina_pagar'),
    
    # Rutas del carro de compras
    path('ver/', views.ver_carrito, name='ver_carrito'),
    path('agregar/<int:juego_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('eliminar/<int:juego_id>/', views.eliminar_del_carrito, name='eliminar_del_carrito'),
    path('gracias/', views.finalizar_compra, name='finalizar_compra'),
    path('actualizar/<int:juego_id>/', views.actualizar_carrito, name='actualizar_carrito'),
]
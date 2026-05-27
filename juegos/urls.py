from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('mas_ventas/', views.mas_ventas, name='mas_ventas'),
    path('nuevos_lanzamientos/', views.nuevos_lanzamientos, name='nuevos_lanzamientos'),
]
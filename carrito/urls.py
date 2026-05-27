from django.urls import path
from . import views

urlpatterns = [
    path('compra/', views.compra, name='compra'),
    path('carro_de_compras/', views.carro_de_compras, name='carro_de_compras'),    
]
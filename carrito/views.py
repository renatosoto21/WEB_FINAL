from django.shortcuts import render

def carro_de_compras(request):
    return render(request, 'carrito/carro_de_compras.html')

def compra(request):
    return render(request, 'carrito/compra.html')



from django.shortcuts import render

def index(request):
    return render(request, 'juegos/index.html')

def mas_ventas(request):
    return render(request, 'juegos/mas_ventas.html')

def nuevos_lanzamientos(request):
    return render(request, 'juegos/nuevos_lanzamientos.html')
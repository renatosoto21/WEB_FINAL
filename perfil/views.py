from django.shortcuts import render

def iniciar_sesion(request):
    return render(request, 'perfil/iniciar_sesion.html')

def registrarse(request):
    return render(request, 'perfil/registrarse.html')

def perfil(request):
    return render(request, 'perfil/perfil.html')
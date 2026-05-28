from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

# 1. VISTA DE PERFIL
def perfil(request):
    return render(request, 'perfil/perfil.html')


# 2. VISTA DE LOGIN (La que estamos usando)
def iniciar_sesion(request):
    error_msg = None
    
    if request.method == 'POST':
        usuario = request.POST.get('username')
        clave = request.POST.get('password')
        
        user = authenticate(request, username=usuario, password=clave)
        
        if user is not None:
            login(request, user)
            if user.is_staff:
                return redirect('panel_admin')
            return redirect('/')
        else:
            error_msg = "Usuario o contraseña incorrectos. Inténtalo de nuevo."
            
    return render(request, 'perfil/iniciar_sesion.html', {'error_msg': error_msg})


# 3. LA FUNCIÓN QUE FALTABA: REGISTRO
def registrarse(request):
    # Dejamos este render básico para que tu servidor vuelva a la vida.
    # Si tenías una lógica compleja aquí antes, puedes reescribirla dentro de esta función.
    return render(request, 'perfil/registrarse.html')
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .forms import UsuarioUpdateForm, PerfilUpdateForm
from .models import Perfil
from juegos.models import Categoria

# 1. VISTA DE PERFIL
def perfil(request):
    categorias = Categoria.objects.all()
    
    contexto = {
        'categorias': categorias,
    }
    
    
    return render(request, 'perfil/perfil.html', contexto)


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
from .forms import RegistroUsuarioForm

def registrarse(request):
    error_msg = None
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/iniciar-sesion/') # Al registrarse, lo mandamos a loguearse
        else:
            error_msg = "Error en el registro. Verifica los datos."
    else:
        form = RegistroUsuarioForm()
        
    return render(request, 'perfil/registrarse.html', {'form': form, 'error_msg': error_msg})

# Asegúrate de que 'logout' esté importado arriba junto a login y authenticate
from django.contrib.auth import logout 

# ... tus otras vistas (perfil, iniciar_sesion, registrarse) ...

# NUEVA VISTA PARA CERRAR SESIÓN
def cerrar_sesion(request):
    logout(request) # Django borra las cookies de sesión del navegador
    return redirect('/') # Nos manda directo a la página principal



@login_required(login_url='/iniciar-sesion/')
def editar_perfil(request):
    # Buscamos el perfil del usuario, o le creamos uno en blanco si no tiene
    perfil, created = Perfil.objects.get_or_create(usuario=request.user)
    categorias = Categoria.objects.all()
    if request.method == 'POST':
        # Recibimos el texto (POST) y la foto (FILES)
        u_form = UsuarioUpdateForm(request.POST, instance=request.user)
        p_form = PerfilUpdateForm(request.POST, request.FILES, instance=request.user.perfil)

        # Si ambos formularios están correctos, guardamos
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect('perfil') # Lo regresamos a ver su perfil actualizado
    else:
        # Si entra por primera vez a editar, cargamos sus datos actuales
        u_form = UsuarioUpdateForm(instance=request.user)
        p_form = PerfilUpdateForm(instance=request.user.perfil)

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'categorias': categorias,
    }
    return render(request, 'perfil/editar_perfil.html', context)
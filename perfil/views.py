from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .forms import UsuarioUpdateForm, PerfilUpdateForm
from .models import Perfil
from juegos.models import Categoria

# 1. VISTA DE PERFIL
def perfil(request):
    categorias = Categoria.objects.all()
    contexto = {'categorias': categorias,}
    
    return render(request, 'perfil/perfil.html', contexto)


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

from .forms import RegistroUsuarioForm

def registrarse(request):
    error_msg = None
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/iniciar-sesion/')
        else:
            error_msg = "Error en el registro. Verifica los datos."
    else:
        form = RegistroUsuarioForm()
        
    return render(request, 'perfil/registrarse.html', {'form': form, 'error_msg': error_msg})

from django.contrib.auth import logout 

def cerrar_sesion(request):
    logout(request) 
    return redirect('/')



@login_required(login_url='/iniciar-sesion/')
def editar_perfil(request):
    
    perfil, created = Perfil.objects.get_or_create(usuario=request.user)
    categorias = Categoria.objects.all()
    if request.method == 'POST':
        u_form = UsuarioUpdateForm(request.POST, instance=request.user)
        p_form = PerfilUpdateForm(request.POST, request.FILES, instance=request.user.perfil)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect('perfil')
    else:
        u_form = UsuarioUpdateForm(instance=request.user)
        p_form = PerfilUpdateForm(instance=request.user.perfil)

    context = {'u_form': u_form,'p_form': p_form,'categorias': categorias,}
    return render(request, 'perfil/editar_perfil.html', context)
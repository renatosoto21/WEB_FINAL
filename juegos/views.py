from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Sum
from .models import Videojuego, Categoria
from .forms import VideojuegoForm, CategoriaForm
from django.contrib.auth.models import User

# ========== VISTAS PÚBLICAS ==========

def index(request):
    ultimos_añadidos = Videojuego.objects.order_by('-fecha_creacion')[:4]
    juegos_en_oferta = Videojuego.objects.filter(en_oferta=True)[:4]
    juegos_destacados = Videojuego.objects.filter(destacado=True)[:4]
    categorias = Categoria.objects.all()

    context = {
        'ultimos': ultimos_añadidos,
        'ofertas': juegos_en_oferta,
        'destacados': juegos_destacados,
        'categorias': categorias,
    }
    return render(request, 'juegos/index.html', context)

def mas_ventas(request):
    categorias = Categoria.objects.all()
    juegos = Videojuego.objects.all()[:10]
    context = {
        'categorias': categorias,
        'juegos': juegos,
    }
    return render(request, 'juegos/mas_ventas.html', context)

def nuevos_lanzamientos(request):
    categorias = Categoria.objects.all()
    juegos = Videojuego.objects.order_by('-fecha_creacion')[:10]
    context = {
        'categorias': categorias,
        'juegos': juegos,
    }
    return render(request, 'juegos/nuevos_lanzamientos.html', context)

def ver_categoria(request, slug):
    categoria = get_object_or_404(Categoria, slug=slug)
    juegos = categoria.videojuegos.all()
    categorias = Categoria.objects.all()

    context = {
        'categoria': categoria,
        'juegos': juegos,
        'categorias': categorias,
    }
    return render(request, 'juegos/categoria_detail.html', context)

def listar_categorias(request):
    categorias = Categoria.objects.all()
    context = {'categorias': categorias}
    return render(request, 'juegos/categorias_list.html', context)

# ========== VISTAS DE AUTENTICACIÓN ==========

def iniciar_sesion(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if user.is_staff:
                    return redirect('panel_admin')
                return redirect('/')
    else:
        form = AuthenticationForm()

    return render(request, '../../perfil/templates/perfil/iniciar_sesion.html', {'form': form})

def cerrar_sesion(request):
    logout(request)
    return redirect('index')

# ========== VISTAS ADMIN - VIDEOJUEGOS ==========

@staff_member_required(login_url='/iniciar-sesion/')
def panel_admin(request):
    videojuegos = Videojuego.objects.all()
    usuarios_registrados = User.objects.all()

    context = {
        'videojuegos': videojuegos,
        'usuarios': usuarios_registrados,
    }
    return render(request, 'juegos/admin/panel_admin.html', context)

@staff_member_required(login_url='/iniciar-sesion/')
def crear_juego(request):
    if request.method == 'POST':
        form = VideojuegoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('panel_admin')
    else:
        form = VideojuegoForm()

    return render(request, 'juegos/admin/form_juego.html', {'form': form, 'accion': 'Agregar'})

@staff_member_required(login_url='/iniciar-sesion/')
def agregar_juego(request):
    if request.method == 'POST':
        form = VideojuegoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('panel_admin')
    else:
        form = VideojuegoForm()

    return render(request, 'juegos/admin/agregar_juego.html', {'form': form})

@staff_member_required(login_url='/iniciar-sesion/')
def editar_juego(request, pk):
    juego = get_object_or_404(Videojuego, pk=pk)

    if request.method == 'POST':
        form = VideojuegoForm(request.POST, request.FILES, instance=juego)
        if form.is_valid():
            form.save()
            return redirect('panel_admin')
    else:
        form = VideojuegoForm(instance=juego)

    return render(request, 'juegos/admin/form_juego.html', {'form': form, 'accion': 'Editar'})

@staff_member_required(login_url='/iniciar-sesion/')
def eliminar_juego(request, pk):
    juego = get_object_or_404(Videojuego, pk=pk)

    if request.method == 'POST':
        juego.delete()
        return redirect('panel_admin')

    return render(request, 'juegos/admin/eliminar_juego.html', {'juego': juego})

# ========== VISTAS ADMIN - CATEGORÍAS ==========

@staff_member_required(login_url='/iniciar-sesion/')
def admin_categorias(request):
    categorias = Categoria.objects.all()
    context = {'categorias': categorias}
    return render(request, 'juegos/admin/admin_categorias.html', context)

@staff_member_required(login_url='/iniciar-sesion/')
def admin_agregar_categoria(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_categorias')
    else:
        form = CategoriaForm()

    return render(request, 'juegos/admin/admin_form_categoria.html', {'form': form, 'accion': 'Agregar'})

@staff_member_required(login_url='/iniciar-sesion/')
def admin_editar_categoria(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)

    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            return redirect('admin_categorias')
    else:
        form = CategoriaForm(instance=categoria)

    return render(request, 'juegos/admin/admin_form_categoria.html', {'form': form, 'accion': 'Editar'})

@staff_member_required(login_url='/iniciar-sesion/')
def admin_eliminar_categoria(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)

    if request.method == 'POST':
        categoria.delete()
        return redirect('admin_categorias')

    return render(request, 'juegos/admin/admin_eliminar_categoria.html', {'categoria': categoria})

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Sum
from .models import Videojuego
from .forms import VideojuegoForm

def index(request):
    return render(request, 'juegos/index.html')

def mas_ventas(request):
    return render(request, 'juegos/mas_ventas.html')

def nuevos_lanzamientos(request):
    return render(request, 'juegos/nuevos_lanzamientos.html')


# 1. Vista del Panel Principal del Administrador
def panel_admin(request):
    
    # Trae todos los videojuegos de la base de datos
    juegos = Videojuego.objects.all()
    
    # --- MÉTRICAS PARA EL DASHBOARD ---
    total_titulos = juegos.count() # Cuenta cuántos juegos hay en total
    total_stock = juegos.aggregate(Sum('stock'))['stock__sum'] or 0 # Suma todas las unidades de stock
    juegos_agotados = juegos.filter(stock=0).count() # Cuenta cuántos tienen stock igual
    
    # Pasamos los datos al HTML en el diccionario de contexto
    context = {
        'juegos': juegos,
        'total_titulos': total_titulos,
        'total_stock': total_stock,
        'juegos_agotados': juegos_agotados
    }
    
    # Se los pasa a la plantilla HTML
    return render(request, 'juegos/panel_admin.html', context)
    return render(request, 'juegos/panel_admin.html', {'juegos': juegos})

# 2. Vista para Agregar un Videojuego Nuevo
def crear_juego(request):
    if request.method == 'POST':
        # request.FILES es OBLIGATORIO para que Pillow reciba la imagen
        form = VideojuegoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save() # Guarda en la base de datos
            return redirect('panel_admin') # Nos manda de vuelta al panel
    else:
        form = VideojuegoForm()
        
    return render(request, 'juegos/form_juego.html', {'form': form, 'accion': 'Agregar'})

# 3. Vista para Editar un juego existente
def editar_juego(request, pk):
    # Busca el juego por su ID (pk), si no existe manda un 404
    juego = get_object_or_404(Videojuego, pk=pk)
    
    if request.method == 'POST':
        # Pasamos instance=juego para que Django sepa que estamos editando ese juego y no creando uno nuevo
        form = VideojuegoForm(request.POST, request.FILES, instance=juego)
        if form.is_valid():
            form.save()
            return redirect('panel_admin')
    else:
        # Rellena el formulario con los datos actuales del juego
        form = VideojuegoForm(instance=juego)
        
    return render(request, 'juegos/form_juego.html', {'form': form, 'accion': 'Editar'})


# 4. Vista para Eliminar un juego
def eliminar_juego(request, pk):
    juego = get_object_or_404(Videojuego, pk=pk)
    
    if request.method == 'POST':
        juego.delete() # Borra de la base de datos
        return redirect('panel_admin')
        
    return render(request, 'juegos/eliminar_juego.html', {'juego': juego})

# 1. VISTA DE LOGIN
def iniciar_sesion(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                # Si es administrador, lo mandamos al dashboard
                if user.is_staff:
                    return redirect('panel_admin')
                # Si es un cliente normal, lo mandamos a la página de inicio
                return redirect('/') 
    else:
        form = AuthenticationForm()
    
    return render(request, 'juegos/login.html', {'form': form})

# 2. VISTA DE LOGOUT (Cerrar sesión)
def cerrar_sesion(request):
    logout(request)
    return redirect('/')

# 3. PROTEGER TU DASHBOARD EXISTENTE
# Agrega este decorador justo arriba de tu función del panel
@staff_member_required(login_url='login')
def panel_admin(request):
    juegos = Videojuego.objects.all()
    total_titulos = juegos.count()
    total_stock = juegos.aggregate(Sum('stock'))['stock__sum'] or 0
    juegos_agotados = juegos.filter(stock=0).count()
    
    context = {
        'juegos': juegos,
        'total_titulos': total_titulos,
        'total_stock': total_stock,
        'juegos_agotados': juegos_agotados
    }
    return render(request, 'juegos/panel_admin.html', context)
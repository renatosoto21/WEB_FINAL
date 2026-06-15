from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Sum
from .models import Videojuego, Categoria
from .forms import VideojuegoForm, CategoriaForm
from django.contrib.auth.models import User
from .models import Videojuego 
from django.http import JsonResponse

# ========== VISTAS PÚBLICAS ==========

def index(request):
    ultimos_añadidos = Videojuego.objects.order_by('-fecha_creacion')[:4]
    juegos_en_oferta = Videojuego.objects.filter(en_oferta=True)[:4]
    juegos_destacados = Videojuego.objects.filter(destacado=True)[:4]
    categorias = Categoria.objects.all()

    # 1. Creamos nuestra lista vacía tradicional
    favoritos_guardados = []
    
    # 2. Validamos si la persona tiene su sesión iniciada
    if request.user.is_authenticated:
        mis_juegos_favoritos = request.user.perfil.juegos_favoritos.all()
        
        # 3. Usamos un ciclo simple para ir guardando número por número (los IDs)
        for juego in mis_juegos_favoritos:
            favoritos_guardados.append(juego.id)

    # 4. Agregamos los favoritos al diccionario (context) que ya tenías
    context = {
        'ultimos': ultimos_añadidos,
        'ofertas': juegos_en_oferta,
        'destacados': juegos_destacados,
        'categorias': categorias,
        'favoritos': favoritos_guardados,  # <--- Aquí va nuestra lista nueva
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

def nuestro_catalogo(request):
    categorias = Categoria.objects.all()
    juegos = Videojuego.objects.order_by('titulo')
    context = {
        'categorias': categorias,
        'juegos': juegos,
    }
    return render(request, 'juegos/nuestro_catalogo.html', context)

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

# Función 1: Muestra la página de favoritos
def ver_favoritos(request):
    print("--- CARGANDO PANTALLA DE FAVORITOS ---")
    if request.user.is_authenticated:
        mis_juegos = request.user.perfil.juegos_favoritos.all()
        print(f"Juegos encontrados: {mis_juegos}")
    else:
        mis_juegos = []
        
    # ¡ESTA LÍNEA ES LA CLAVE! Si no tiene el diccionario al final, el HTML no sabrá qué mostrar
    return render(request, 'juegos/favoritos.html', {'mis_juegos': mis_juegos})


# Función 2: Atrapa el ID, guarda el juego y avisa a JavaScript el color
def agregar_favorito(request, juego_id):
    print(f"--- INTENTANDO AGREGAR JUEGO ID: {juego_id} ---") # Chismoso 1

    if request.user.is_authenticated:
        print(f"Usuario detectado: {request.user.username}") # Chismoso 2

        juego_seleccionado = get_object_or_404(Videojuego, id=juego_id)

        if juego_seleccionado in request.user.perfil.juegos_favoritos.all():
            request.user.perfil.juegos_favoritos.remove(juego_seleccionado)
            print("Resultado: El juego ya estaba, así que lo QUILTE.") # Chismoso 3
        else:
            request.user.perfil.juegos_favoritos.add(juego_seleccionado)
            print("Resultado: Juego AGREGADO exitosamente a la base de datos.") # Chismoso 4
    else:
        print("ERROR: El sistema dice que el usuario NO ha iniciado sesión.") # Chismoso 5

    return redirect(request.META.get('HTTP_REFERER', 'index'))


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
    categorias = Categoria.objects.all()

    context = {
        'videojuegos': videojuegos,
        'usuarios': usuarios_registrados,
        'categorias': categorias,
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
def crear_categoria(request):
    if request.method == 'POST':
        nombre_recibido = request.POST.get('nombre') # Captura lo que se escribió en el input
        
        if nombre_recibido:
            # Creamos el registro en la base de datos
            Categoria.objects.create(nombre=nombre_recibido)
            
    return redirect('panel_admin') # Regresa al panel con los datos actualizados

@staff_member_required(login_url='/iniciar-sesion/')
def editar_categoria(request, cat_id):
    # Buscamos la categoría o devolvemos error 404 si no existe
    categoria = get_object_or_404(Categoria, id=cat_id)
    
    if request.method == 'POST':
        # Capturamos el nuevo nombre del formulario
        nuevo_nombre = request.POST.get('nuevo_nombre')
        if nuevo_nombre:
            categoria.nombre = nuevo_nombre
            categoria.save()
            
    # Siempre redirigimos al panel, ya sea después de editar o si alguien entró por accidente
    return redirect('panel_admin')

@staff_member_required(login_url='/iniciar-sesion/')
def eliminar_categoria(request, cat_id):
    # Buscamos la categoría y la borramos de una
    categoria_a_borrar = Categoria.objects.get(id=cat_id)
    categoria_a_borrar.delete()
    
    return redirect('panel_admin')

@staff_member_required(login_url='/iniciar-sesion/')
def eliminar_usuario(request, user_id):
    # Buscamos al usuario en la base de datos
    usuario_a_eliminar = User.objects.get(id=user_id)
    
    # Doble chequeo de seguridad: que el usuario que intenta borrar no sea él mismo
    if request.user.id != usuario_a_eliminar.id:
        usuario_a_eliminar.delete() # ¡Adiós usuario!
        
    # Redirigimos de vuelta al panel de admin
    return redirect('panel_admin') # Cambia 'panel_admin' si el nombre de tu URL es distinto


# VISTA DETALLE DE JUEGO (PÚBLICA)
def detalle_juego(request, juego_id):
    juego = get_object_or_404(Videojuego, id=juego_id)
    
    # Buscamos 4 juegos cualquiera para la zona de "Similares"
    # Usamos exclude para no recomendar el mismo juego que ya estamos viendo
    juegos_similares = Videojuego.objects.exclude(id=juego_id)[0:4]
    
    contexto = {
        'juego': juego,
        'similares': juegos_similares
    }
    
    return render(request, 'juegos/detalle_juego.html', contexto)


def buscar(request):
    # 1. Atrapamos lo que el usuario escribió (la variable 'q')
    texto_busqueda = request.GET.get('q', '')
    
    # 2. Creamos una lista vacía por si no encuentra nada
    juegos_encontrados = []
    
    # 3. Si el usuario escribió algo, buscamos en la base de datos
    if texto_busqueda:
        # __icontains busca si el texto está en cualquier parte del título (sin importar mayúsculas)
        juegos_encontrados = Videojuego.objects.filter(titulo__icontains=texto_busqueda)
        
    contexto = {
        'juegos': juegos_encontrados,
        'texto_busqueda': texto_busqueda
    }
    
    return render(request, 'juegos/resultados_busqueda.html', contexto)



def buscar_en_vivo(request):
    texto = request.GET.get('q', '')
    juegos_lista = []
    
    if texto != '':
        juegos = Videojuego.objects.filter(titulo__icontains=texto)[0:5]
        
        for juego in juegos:
            # 1. Creamos una variable simple para guardar la ruta de la foto
            ruta_foto = ""
            
            # 2. Si el juego tiene imagen guardada, obtenemos su URL
            if juego.imagen:
                ruta_foto = juego.imagen.url
                
            # 3. Agregamos la foto a nuestro diccionario
            diccionario = {
                'id': juego.id,
                'titulo': juego.titulo,
                'imagen': ruta_foto
            }
            juegos_lista.append(diccionario)
            
    return JsonResponse(juegos_lista, safe=False)

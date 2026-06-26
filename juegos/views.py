from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Sum
from .models import Videojuego, Categoria
from .forms import VideojuegoForm, CategoriaForm
from django.contrib.auth.models import User
from .models import Videojuego, Categoria, Compra
from django.http import JsonResponse

# ========== VISTAS PÚBLICAS ==========

def index(request):
    ultimos_añadidos = Videojuego.objects.filter(activo=True).order_by('-fecha_creacion')[:4]  
    juegos_en_oferta = Videojuego.objects.filter(en_oferta=True, activo=True)[:4]
    juegos_destacados = Videojuego.objects.filter(destacado=True, activo=True)[:4]
    categorias = Categoria.objects.all()

#guardar los juegos favoritos 
    favoritos_guardados = []
    if request.user.is_authenticated:
        mis_juegos_favoritos = request.user.perfil.juegos_favoritos.all()
        for juego in mis_juegos_favoritos:
            favoritos_guardados.append(juego.id)

    contexto = {'ultimos': ultimos_añadidos,'ofertas': juegos_en_oferta,'destacados': 
                juegos_destacados,'categorias': categorias,'favoritos_ids': favoritos_guardados,}
    
    return render(request, 'juegos/index.html', contexto)

def mas_ventas(request):
    categorias = Categoria.objects.all()
    juegos = Videojuego.objects.filter(activo=True)[:99]
    ofertas = Videojuego.objects.filter(en_oferta=True, activo=True)[:99]
    favoritos_guardados = []

    #Validamos si la persona tiene su sesión iniciada
    if request.user.is_authenticated:
        mis_juegos_favoritos = request.user.perfil.juegos_favoritos.all()
        
        for juego in mis_juegos_favoritos:
            favoritos_guardados.append(juego.id)
    
    context = {'categorias': categorias,'juegos': juegos,'ofertas': ofertas,'favoritos_ids': favoritos_guardados, }
    return render(request, 'juegos/mas_ventas.html', context)


def nuevos_lanzamientos(request):
    categorias = Categoria.objects.all()
    juegos = Videojuego.objects.filter(activo=True).order_by('-fecha_creacion')[:99]
    juegos_destacados = Videojuego.objects.filter(destacado=True, activo=True)[:99]
    favoritos_guardados = []
    
    if request.user.is_authenticated:
        mis_juegos_favoritos = request.user.perfil.juegos_favoritos.all()
        
        for juego in mis_juegos_favoritos:
            favoritos_guardados.append(juego.id)
    context = {'categorias': categorias,'juegos': juegos,'destacados': juegos_destacados,'favoritos_ids': favoritos_guardados, }
    return render(request, 'juegos/nuevos_lanzamientos.html', context)

def nuestro_catalogo(request):
    categorias = Categoria.objects.all()
    juegos = Videojuego.objects.filter(activo=True).order_by('titulo')
    favoritos_guardados = []
    
    if request.user.is_authenticated:
        mis_juegos_favoritos = request.user.perfil.juegos_favoritos.all()
        
        for juego in mis_juegos_favoritos:
            favoritos_guardados.append(juego.id)
            
    context = {'categorias': categorias,'juegos': juegos,'favoritos_ids': favoritos_guardados,}
    return render(request, 'juegos/nuestro_catalogo.html', context)


def ver_categoria(request, slug):
    categoria = get_object_or_404(Categoria, slug=slug)
    juegos = categoria.videojuegos.filter(activo=True)
    categorias = Categoria.objects.all()
          
    favoritos_guardados = []
    
    if request.user.is_authenticated:
        mis_juegos_favoritos = request.user.perfil.juegos_favoritos.all()
        
        for juego in mis_juegos_favoritos:
            favoritos_guardados.append(juego.id)
            
    context = {'categoria': categoria,'juegos': juegos,'categorias': categorias,'favoritos_ids': favoritos_guardados,}
    return render(request, 'juegos/categoria_detail.html', context)



def listar_categorias(request):
    categorias = Categoria.objects.all()
    context = {'categorias': categorias}
    return render(request, 'juegos/categorias_list.html', context)


def ver_favoritos(request):
    categorias = Categoria.objects.all()
    print("--- CARGANDO PANTALLA DE FAVORITOS ---")

    if request.user.is_authenticated:
        mis_juegos = request.user.perfil.juegos_favoritos.all()
        print(f"Juegos encontrados: {mis_juegos}")
    else:
        mis_juegos = []
        
    contexto = {'categorias': categorias,'mis_juegos': mis_juegos,}   
    return render(request, 'juegos/favoritos.html', contexto)


def agregar_favorito(request, juego_id):
    if request.user.is_authenticated:
        juego_seleccionado = get_object_or_404(Videojuego, id=juego_id)

        if juego_seleccionado in request.user.perfil.juegos_favoritos.all():
            request.user.perfil.juegos_favoritos.remove(juego_seleccionado)
        else:
            request.user.perfil.juegos_favoritos.add(juego_seleccionado)
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
    total_juegos = Videojuego.objects.count()
    total_vendidos = Compra.objects.count()
    ultimas_ventas = Compra.objects.all().order_by('-fecha_compra')[:99]
    videojuegos = Videojuego.objects.all()
    usuarios_registrados = User.objects.all()
    categorias = Categoria.objects.all()

    context = {'videojuegos': videojuegos,'usuarios': usuarios_registrados,'categorias': categorias,'total_juegos': total_juegos,
               'total_vendidos': total_vendidos,'ultimas_ventas': ultimas_ventas,}
    
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
    #solamente elimina juegos si no tiene ventas
def eliminar_juego(request, pk):
    juego = Videojuego.objects.get(id=pk)
    tiene_ventas = Compra.objects.filter(juego=juego).exists()
    if tiene_ventas:
        juego.activo = False
        juego.save()
    else:
        juego.delete()
    return redirect('panel_admin')

#  VISTAS ADMIN - CATEGORÍAS 

@staff_member_required(login_url='/iniciar-sesion/')
def admin_categorias(request):
    categorias = Categoria.objects.all()
    context = {'categorias': categorias}
    return render(request, 'juegos/admin/admin_categorias.html', context)

@staff_member_required(login_url='/iniciar-sesion/')
def crear_categoria(request):
    if request.method == 'POST':
        nombre_recibido = request.POST.get('nombre') 
        if nombre_recibido:
            Categoria.objects.create(nombre=nombre_recibido)
    return redirect('panel_admin')

@staff_member_required(login_url='/iniciar-sesion/')
def editar_categoria(request, cat_id):
    categoria = get_object_or_404(Categoria, id=cat_id)
    
    if request.method == 'POST':
        nuevo_nombre = request.POST.get('nuevo_nombre')
        if nuevo_nombre:
            categoria.nombre = nuevo_nombre
            categoria.save()
    return redirect('panel_admin')

@staff_member_required(login_url='/iniciar-sesion/')
def eliminar_categoria(request, cat_id):
    categoria_a_borrar = Categoria.objects.get(id=cat_id)
    categoria_a_borrar.delete()
    
    return redirect('panel_admin')

@staff_member_required(login_url='/iniciar-sesion/')
def eliminar_usuario(request, user_id):
    usuario_a_eliminar = User.objects.get(id=user_id)
    
    if request.user.id != usuario_a_eliminar.id:
        usuario_a_eliminar.delete() 
        
    return redirect('panel_admin') 


# VISTA DETALLE DE JUEGO (PÚBLICA)
def detalle_juego(request, juego_id):
    juego_actual = get_object_or_404(Videojuego, id=juego_id)
    lista_similares = Videojuego.objects.filter(categoria=juego_actual.categoria).exclude(id=juego_actual.id)[0:4]
    lista_categorias = Categoria.objects.all()

    contexto = {'juego': juego_actual,'similares': lista_similares, 'categorias': lista_categorias, }

    return render(request, 'juegos/detalle_juego.html', contexto)


def buscar(request):
    texto_busqueda = request.GET.get('q', '')
    juegos_encontrados = []
    
    if texto_busqueda:
        juegos_encontrados = Videojuego.objects.filter(titulo__icontains=texto_busqueda, activo=True)
        
    contexto = {'juegos': juegos_encontrados,'texto_busqueda': texto_busqueda}
    return render(request, 'juegos/resultados_busqueda.html', contexto)



def buscar_en_vivo(request):
    texto = request.GET.get('q', '')
    juegos_lista = []
    
    if texto != '':
        juegos = Videojuego.objects.filter(titulo__icontains=texto, activo=True)[0:5]
        
        for juego in juegos:
            ruta_foto = ""
            if juego.portada:
                ruta_foto = juego.portada.url
            diccionario = {'id': juego.id,'titulo': juego.titulo,'portada': ruta_foto}
            juegos_lista.append(diccionario)
            
    return JsonResponse(juegos_lista, safe=False)



def historial_compras(request):
    if not request.user.is_authenticated:
        return redirect('index') 
    compras = Compra.objects.filter(usuario=request.user).order_by('-fecha_compra')
    
    return render(request, 'juegos/historial_compras.html', {'compras': compras})



def procesar_compra_directa(request, juego_id):
    if not request.user.is_authenticated:
        return redirect('login')
        
    if request.method == 'POST' or request.method == 'GET':
        juego = get_object_or_404(Videojuego, id=juego_id)
        
        Compra.objects.create(
            usuario=request.user,
            juego=juego,
            precio_pagado=juego.precio 
        )   
        return redirect('historial_compras')


# --- PÁGINAS DE SOPORTE ---

def preguntas_frecuentes(request):
    lista_categorias = Categoria.objects.all()
    contexto = {'categorias': lista_categorias}
    return render(request, 'juegos/preguntas_frecuentes.html', contexto)

def terminos_servicio(request):
    lista_categorias = Categoria.objects.all()
    contexto = {'categorias': lista_categorias}
    return render(request, 'juegos/terminos_servicio.html', contexto)

def politica_privacidad(request):
    lista_categorias = Categoria.objects.all()
    contexto = {'categorias': lista_categorias}
    return render(request, 'juegos/politica_privacidad.html', contexto)
from django.shortcuts import render, redirect
from juegos.models import Videojuego 


def compra(request):
    return render(request, 'carrito/compra.html')



def ver_carrito(request):
    carro = request.session.get('carro', {})
    juegos_guardados = [] 
    total_precio = 0
    
    for key, valor in carro.items():
        # Guardamos el ID real dentro del diccionario temporal para usarlo en el botón de eliminar
        valor['id'] = key  
        juegos_guardados.append(valor)
        
        subtotal_juego = valor['precio'] * valor['cantidad']
        total_precio = total_precio + subtotal_juego
        
    contexto = {
        'juegos_en_carrito': juegos_guardados,
        'total': total_precio
    }
    return render(request, 'carrito/carro_de_compras.html', contexto)

def procesar_pago(request):
    carro = request.session.get('carro', {})
    
    precio_total = 0
    
    # Sumamos el precio de los juegos
    for key, valor in carro.items():
        subtotal_juego = valor['precio'] * valor['cantidad']
        precio_total = precio_total + subtotal_juego
        
    # Empaquetamos solo el total
    contexto = {
        'total': precio_total
    }
    
    return render(request, 'carrito/compra.html', contexto)

def agregar_al_carrito(request, juego_id):
    carro = request.session.get('carro', {})
    juego = Videojuego.objects.get(id=juego_id)
    id_texto = str(juego_id)
    
    if id_texto in carro:
        carro[id_texto]['cantidad'] = carro[id_texto]['cantidad'] + 1
    else:
        # Hacemos un if muy simple para guardar la ruta de la imagen si es que tiene una
        ruta_imagen = ""
        if juego.imagen:
            ruta_imagen = juego.imagen.url
            
        # Agregamos la variable 'imagen' al diccionario
        carro[id_texto] = {
            'titulo': juego.titulo,
            'precio': int(juego.precio),
            'cantidad': 1,
            'imagen': ruta_imagen  # <-- ¡Esta es la línea nueva!
        }
        
    request.session['carro'] = carro
    request.session.modified = True
    
    return redirect('ver_carrito')

def eliminar_del_carrito(request, juego_id):
    # 1. Traemos el carrito actual de la sesión
    carro = request.session.get('carro', {})
    id_texto = str(juego_id)
    
    # 2. Si el juego existe en el carrito, lo borramos
    if id_texto in carro:
        del carro[id_texto]
        
    # 3. Guardamos los cambios en la sesión
    request.session['carro'] = carro
    request.session.modified = True
    
    # 4. Redirigimos de vuelta a la pantalla del carrito para ver los cambios
    return redirect('ver_carrito')

def finalizar_compra(request):
    # Dejamos el carrito vacío en la memoria porque la compra ya se completó
    request.session['carro'] = {}
    request.session.modified = True
    
    # Mostramos la página de gracias
    return render(request, 'carrito/gracias.html')



def finalizar_compra(request):
    # 1. Obtenemos el carro actual de la memoria de la sesión
    carro = request.session.get('carro', {})
    
    # 2. Recorremos cada juego que está dentro del carro
    for juego_id, info in carro.items():
        try:
            # Buscamos el juego real en la base de datos usando su ID
            juego_db = Videojuego.objects.get(id=int(juego_id))
            
            # Restamos el stock actual menos la cantidad comprada
            juego_db.stock = juego_db.stock - info['cantidad']
            
            # Si por alguna razón el stock da negativo, lo dejamos en 0 para que no se vea feo
            if juego_db.stock < 0:
                juego_db.stock = 0
                
            # Guardamos los cambios de este juego en la base de datos
            juego_db.save()
            
        except Videojuego.DoesNotExist:
            # Si el juego ya no existe en la base de datos, simplemente continúa con el siguiente
            continue

    # 3. Una vez que ya restamos el stock de todos, ahora sí vaciamos el carro
    request.session['carro'] = {}
    request.session.modified = True
    
    # 4. Mostramos la pantalla de agradecimiento centrado que editamos antes
    return render(request, 'carrito/gracias.html')
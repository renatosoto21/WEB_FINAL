from django.shortcuts import render, redirect
from juegos.models import Videojuego
from juegos.models import Videojuego, Compra, Categoria
from django.core.mail import send_mail

def compra(request):
    return render(request, 'carrito/compra.html')

def ver_carrito(request):
    carro = request.session.get('carro', {})
    juegos_guardados = [] 
    total_precio = 0
    categorias = Categoria.objects.all()
    
    for key, valor in carro.items():
        valor['id'] = key  
        
        try:
            # Buscamos el juego en la Base de Datos con tus modelos exactos
            juego_db = Videojuego.objects.get(id=int(key))
            
            # Pasamos las propiedades del modelo al diccionario del carro
            valor['en_oferta'] = juego_db.en_oferta
            valor['precio_oferta'] = juego_db.precio_oferta if juego_db.precio_oferta else 0
            valor['precio'] = juego_db.precio # Mantiene el precio original para el <strike>
            
        except Videojuego.DoesNotExist:
            valor['en_oferta'] = False
            valor['precio_oferta'] = 0
        
        juegos_guardados.append(valor)
        
        # Si está en oferta, calcula el total usando el precio de oferta
        if valor['en_oferta']:
            subtotal_juego = valor['precio_oferta'] * valor['cantidad']
        else:
            subtotal_juego = valor['precio'] * valor['cantidad']
            
        total_precio = total_precio + subtotal_juego
        
    contexto = {
        'juegos_en_carrito': juegos_guardados,
        'total': total_precio,
        'categorias': categorias,
    }
    return render(request, 'carrito/carro_de_compras.html', contexto)

def procesar_pago(request):
    carro = request.session.get('carro', {})
    precio_total = 0
    
    # Sumamos el precio de los juegos
    for key, valor in carro.items():
            try:
                juego_db = Videojuego.objects.get(id=int(key))
                
                # Verificamos cuál es el precio real a cobrar en este momento
                if juego_db.en_oferta and juego_db.precio_oferta:
                    precio_real = juego_db.precio_oferta
                else:
                    precio_real = juego_db.precio
                    
            except Videojuego.DoesNotExist:
                # Si hay un error, usamos el precio base guardado
                precio_real = valor.get('precio', 0)
                
            subtotal_juego = precio_real * valor['cantidad']
            precio_total = precio_total + subtotal_juego
        
    contexto = {
        'total': precio_total
    }
    
    return render(request, 'carrito/compra.html', contexto)

def agregar_al_carrito(request, juego_id):
    carro = request.session.get('carro', {})
    juego = Videojuego.objects.get(id=juego_id)
    id_texto = str(juego_id)

    # CANDADO 1: Que el juego tenga al menos 1 unidad en la tienda
    if juego.stock > 0:
        
        if id_texto in carro:
            # CANDADO 2 (¡EL NUEVO!): Solo sumamos si lo que ya tengo en el carro es MENOR al stock real
            if carro[id_texto]['cantidad'] < juego.stock:
                carro[id_texto]['cantidad'] = carro[id_texto]['cantidad'] + 1
            else:
                # Si la cantidad en el carro ya es igual al stock, ignoramos el clic y no sumamos más
                pass
        else:
            # Si el juego no estaba en el carro, lo agregamos por primera vez con cantidad 1
            ruta_portada = ""
            if juego.portada:
                ruta_portada = juego.portada.url
            
            carro[id_texto] = {
                'titulo': juego.titulo,
                'precio': int(juego.precio),
                'cantidad': 1,
                'portada': ruta_portada 
            }

        if request.user.is_authenticated:
            request.user.perfil.juegos_favoritos.remove(juego)

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
    carro = request.session.get('carro', {})
    
    # 1. Tu mensaje de texto normal (de respaldo por si falla el HTML)
    mensaje_recibo = "¡Hola! Gracias por tu compra en Gaming Store.\n\nAquí tienes el detalle de tu pedido:\n\n"
    
    # 2. Tu versión HTML con diseño oscuro y tu logo neón
    mensaje_html = """""
    <html>
        <body style="font-family: Arial, sans-serif; background-color: #0b0612; color: #ffffff; padding: 20px;">
            <div style="text-align: center; margin-bottom: 25px;">
                
                <img src="https://i.postimg.cc/1zcjQvBj/logogo.png" alt="Gaming Store Logo" style="width: 280px; max-width: 100%; height: auto;">
                
            </div>
            <h2 style="color: #00ffff; text-align: center; font-size: 24px; margin-bottom: 20px;">¡Gracias por tu compra! 🎮</h2>
            <p style="color: #e0e0e0; font-size: 16px;">Aquí tienes el detalle de tu pedido:</p>
            <ul style="list-style-type: none; padding: 0;">
    """

    for juego_id, info in carro.items():
        try:
            juego_db = Videojuego.objects.get(id=int(juego_id))
            juego_db.stock = juego_db.stock - info['cantidad']
            
            if juego_db.stock < 0:
                juego_db.stock = 0
            juego_db.save()
            
            if request.user.is_authenticated:
                for _ in range(info['cantidad']):
                    Compra.objects.create(
                        usuario=request.user,
                        juego=juego_db,
                        precio_pagado=info['precio']
                    )
            
            # Sumamos al texto normal
            mensaje_recibo += f"- {info['cantidad']}x {info['titulo']} (Pagado: ${info['precio']})\n"
            
            # Sumamos al HTML (con diseño estilizado de lista)
            mensaje_html += f"""
            <li style='padding: 12px; border-bottom: 1px solid #2a1b40; background-color: #130924; margin-bottom: 5px; border-radius: 4px;'>
                <span style='color: #00ffff; font-weight: bold;'>{info['cantidad']}x</span> <b style='color: #ffffff;'>{info['titulo']}</b> - <span style='color: #ff00ff; font-weight: bold;'>${info['precio']}</span>
            </li>
            """
            
        except Videojuego.DoesNotExist:
            continue

    # Cerramos ambos mensajes
    mensaje_recibo += "\n¡Que disfrutes tus juegos!\nEl equipo de Gaming Store."
    mensaje_html += """
            </ul>
            <p style="text-align: center; margin-top: 35px; color: #a0a4b0; font-size: 15px;">¡Que disfrutes tus juegos!</p>
            <p style="text-align: center; font-weight: bold; color: #9d4edd; font-size: 16px; margin-top: 5px;">El equipo de Gaming Store.</p>
        </body>
    </html>
    """
    
    if request.user.is_authenticated and request.user.email:
        try:
            send_mail(
                subject='Tu recibo de compra - Gaming Store',
                message=mensaje_recibo, 
                from_email='gamingstore20261@gmail.com',  
                recipient_list=[request.user.email],
                fail_silently=False,
                html_message=mensaje_html, 
            )
        except Exception as e:
            print(f"Error al enviar el correo: {e}")

    request.session['carro'] = {}
    request.session.modified = True
    
    return render(request, 'carrito/gracias.html')
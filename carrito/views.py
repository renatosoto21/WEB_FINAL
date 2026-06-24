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
          
            juego_db = Videojuego.objects.get(id=int(key))
            

            valor['en_oferta'] = juego_db.en_oferta
            valor['precio_oferta'] = juego_db.precio_oferta if juego_db.precio_oferta else 0
            valor['precio'] = juego_db.precio 
            
        except Videojuego.DoesNotExist:
            valor['en_oferta'] = False
            valor['precio_oferta'] = 0
        
        juegos_guardados.append(valor)
       
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
    
    for key, valor in carro.items():
            try:
                juego_db = Videojuego.objects.get(id=int(key))
                
              
                if juego_db.en_oferta and juego_db.precio_oferta:
                    precio_real = juego_db.precio_oferta
                else:
                    precio_real = juego_db.precio
                    
            except Videojuego.DoesNotExist:
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
 
    if juego.stock > 0:
        
        if id_texto in carro:
        
            if carro[id_texto]['cantidad'] < juego.stock:
                carro[id_texto]['cantidad'] = carro[id_texto]['cantidad'] + 1
            else:
                pass
        else:
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
    carro = request.session.get('carro', {})
    id_texto = str(juego_id)
    

    if id_texto in carro:
        del carro[id_texto]
        
    request.session['carro'] = carro
    request.session.modified = True
    
    return redirect('ver_carrito')



def finalizar_compra(request):
    carro = request.session.get('carro', {})
    
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
                    
        except Videojuego.DoesNotExist:
            continue

    request.session['carro'] = {}
    request.session.modified = True
    
    return render(request, 'carrito/gracias.html')
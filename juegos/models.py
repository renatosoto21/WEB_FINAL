from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User

class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, null=True, blank=True)
    descripcion = models.TextField(null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['nombre']
        verbose_name_plural = "Categorías"

    def __str__(self):
        return self.nombre
    
    #valida que el slug sea unico y no se repita
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nombre)
        super().save(*args, **kwargs)

class Videojuego(models.Model):
    titulo = models.CharField(max_length=100)
    plataforma = [('PS5', 'PlayStation 5'),('Xbox Series X', 'Xbox Series X'),
                   ('Nintendo Switch', 'Nintendo Switch'),('PS4', 'PlayStation 4'),
                   ('Xbox One', 'Xbox One'),('Xbox Tresesenta','Xbox 360'),]
    
    plataforma = models.CharField(max_length=50, choices=plataforma, default='PS5')
    descripcion = models.TextField()
    precio = models.IntegerField()
    stock = models.IntegerField(default=0)
    portada = models.ImageField(upload_to='portadas/', null=True, blank=True)
    
    # Imágenes adicionales para el detalle del juego
    imagen1 = models.ImageField(upload_to='juegos/', null=True, blank=True)
    imagen2 = models.ImageField(upload_to='juegos/', null=True, blank=True)
    imagen3 = models.ImageField(upload_to='juegos/', null=True, blank=True)

    fecha_creacion = models.DateTimeField(auto_now_add=True)
    en_oferta = models.BooleanField(default=False)
    precio_oferta = models.IntegerField(null=True, blank=True)
    fecha_oferta = models.DateTimeField(null=True, blank=True)
    destacado = models.BooleanField(default=False)
    fecha_destacado = models.DateTimeField(null=True, blank=True)
    url= models.CharField(max_length=200, null=True, blank=True)
    activo = models.BooleanField(default=True)
    categoria = models.ForeignKey(Categoria,on_delete=models.SET_NULL,null=True,blank=True,related_name='videojuegos')

    def __str__(self):
        return self.titulo
    
class Compra(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mis_compras')
    juego = models.ForeignKey(Videojuego, on_delete=models.SET_NULL, null=True)
    precio_pagado = models.IntegerField()
    fecha_compra = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.usuario.username} compró {self.juego.titulo}"
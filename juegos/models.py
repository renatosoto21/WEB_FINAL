from django.db import models

class Videojuego(models.Model):
    # El título del juego
    titulo = models.CharField(max_length=100)
    
    # Una descripción detallada del juego
    descripcion = models.TextField()
    
    # El precio (usamos IntegerField para simplificar, ideal para CLP, MXN, etc.)
    precio = models.IntegerField()
    
    # Cuántos juegos tienes disponibles en inventario
    stock = models.IntegerField(default=0)
    
    # Aquí entra Pillow. Las imágenes se guardarán en una carpeta llamada 'portadas'
    imagen = models.ImageField(upload_to='portadas/', null=True, blank=True)
    
    # Guarda la fecha exacta en la que se subió el juego automáticamente
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    # Esto sirve para que en el panel de Django veas el nombre del juego y no un texto raro
    def __str__(self):
        return self.titulo
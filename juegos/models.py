from django.db import models

class Videojuego(models.Model):
    titulo = models.CharField(max_length=100)
    
    descripcion = models.TextField()
    
    precio = models.IntegerField()
    
    stock = models.IntegerField(default=0)
    
    imagen = models.ImageField(upload_to='portadas/', null=True, blank=True)
    
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo
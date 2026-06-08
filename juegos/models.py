from django.db import models
from django.utils.text import slugify

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

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nombre)
        super().save(*args, **kwargs)

class Videojuego(models.Model):
    titulo = models.CharField(max_length=100)

    PLATAFORMAS = [
        ('PC', 'PC'),
        ('PS5', 'PlayStation 5'),
        ('Xbox Series X', 'Xbox Series X'),
        ('Nintendo Switch', 'Nintendo Switch'),
        ('PS4', 'PlayStation 4'),
        ('Xbox One', 'Xbox One'),
    ]
    plataforma = models.CharField(max_length=50, choices=PLATAFORMAS, default='PC')

    
    descripcion = models.TextField()
    
    precio = models.IntegerField()
    
    stock = models.IntegerField(default=0)
    
    imagen = models.ImageField(upload_to='portadas/', null=True, blank=True)
    
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    en_oferta = models.BooleanField(default=False)

    destacado = models.BooleanField(default=False)

    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='videojuegos'
    )

    def __str__(self):
        return self.titulo
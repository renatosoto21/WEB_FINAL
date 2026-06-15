from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

class Perfil(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)

    foto_perfil = models.ImageField(upload_to='fotos_perfil/', blank=True, null=True)
    juegos_favoritos = models.ManyToManyField('juegos.Videojuego', blank=True)

    def __str__(self):
        return f"Perfil de {self.usuario.username}"
    
# 2. Creamos la señal para fabricar el perfil automáticamente
@receiver(post_save, sender=User)
def crear_perfil_usuario(sender, instance, created, **kwargs):
    # Si el usuario es nuevo (created es True), le creamos su Perfil
    if created:
        # CAMBIAMOS 'user=' POR 'usuario=' para que coincida con tu modelo
        Perfil.objects.create(usuario=instance) 

# 3. Esta señal guarda el perfil si el usuario se actualiza
@receiver(post_save, sender=User)
def guardar_perfil_usuario(sender, instance, **kwargs):
    instance.perfil.save()
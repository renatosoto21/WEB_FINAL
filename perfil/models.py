from django.db import models
from django.contrib.auth.models import User 

class Perfil(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)

    foto_perfil = models.ImageField(upload_to='fotos_perfil/', blank=True, null=True)
    def __str__(self):
        return f"Perfil de {self.usuario.username}"
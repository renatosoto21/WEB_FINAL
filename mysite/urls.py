"""
(El mapa de tu sitio web):
Este archivo maneja las rutas de tu página. Aquí defines a dónde debe ir un usuario cuando escribe una dirección web. 
Por ejemplo, aquí es donde le dices a Django: "Si el usuario entra a la ruta /juegos/, envíalo a la sección del catálogo".
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('juegos.urls')),
    path('', include('perfil.urls')),
    path('carrito/', include('carrito.urls')),
]

# Forzamos a Django a servir tanto MEDIA como STATIC en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.BASE_DIR / 'static')
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from juegos.models import Categoria
from django.utils.text import slugify

categorias_nombres = [
    'Acción',
    'Aventura',
    'Metroidvania',
    'Shooters',
    'Estrategia',
    'Simulación',
    'Mundo Abierto',
    'Peleas',
    'Novela visual',
    'Puzzle',
    'Deportes',
    'Carreras', 
    'Juegos de Mesa',
]

print("Cargando categorias...")
for nombre in categorias_nombres:
    categoria, created = Categoria.objects.get_or_create(
        nombre=nombre,
        defaults={'slug': slugify(nombre)}
    )
    if created:
        print("[+] Categoria '{}' creada".format(nombre))
    else:
        print("[-] Categoria '{}' ya existe".format(nombre))

print("\n[OK] Categorias cargadas exitosamente")

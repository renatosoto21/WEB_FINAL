from django.contrib import admin
from .models import Videojuego, Categoria
from .models import Videojuego, Compra

class VideojuegoInline(admin.TabularInline):
    model = Videojuego
    extra = 0
    fields = ['titulo', 'precio', 'stock']

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'get_juegos_count', 'fecha_creacion']
    search_fields = ['nombre']
    prepopulated_fields = {'slug': ('nombre',)}

    def get_juegos_count(self, obj):
        return obj.videojuegos.count()
    get_juegos_count.short_description = 'Cantidad de Juegos'

    inlines = [VideojuegoInline]

@admin.register(Videojuego)
class VideojuegoAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'categoria', 'precio', 'stock', 'en_oferta','plataforma']
    list_filter = ['categoria', 'en_oferta', 'destacado', 'fecha_creacion']
    search_fields = ['titulo', 'descripcion']
    fieldsets = (
        ('Información Básica', {
            'fields': ('titulo', 'descripcion', 'categoria')
        }),
        ('Precios y Stock', {
            'fields': ('precio', 'stock', 'en_oferta', 'precio_oferta')
        }),
        ('Imagenes', {
            'fields': ('portada', 'imagen1', 'imagen2', 'imagen3')
        }),
        ('Estado', {
            'fields': ('destacado', )
        }),
    )
    admin.site.register(Compra)
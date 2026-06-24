from django import forms
from .models import Videojuego, Categoria
from django.core.exceptions import ValidationError

class VideojuegoForm(forms.ModelForm):
    class Meta:
        model = Videojuego
        fields = ['titulo', 'descripcion', 'precio', 'stock', 'portada', 'imagen1', 'imagen2', 'imagen3', 'categoria','plataforma','precio_oferta', 'en_oferta', 'destacado', 'url', 'activo']
        labels = {'url': 'URL'}
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'precio': forms.NumberInput(attrs={'class': 'form-control'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control'}),
            'portada': forms.FileInput(attrs={'class': 'form-control'}),
            'imagen1': forms.FileInput(attrs={'class': 'form-control'}),
            'imagen2': forms.FileInput(attrs={'class': 'form-control'}),
            'imagen3': forms.FileInput(attrs={'class': 'form-control'}),
            'categoria': forms.Select(attrs={'class': 'form-control'}),
            'plataforma': forms.Select(attrs={'class': 'form-control'}),
            'url': forms.URLInput(attrs={'class': 'form-control'}),
        }

    #comvierte los link de youtube en embed para que no de error al momento de mostrar el video en la pagina
    def clean_url(self):
        enlace = self.cleaned_data.get('url')
        if enlace and 'watch?v=' in enlace:
            enlace = enlace.replace('watch?v=', 'embed/')
        return enlace
    
    #valida que el precio, stock y precio de oferta no sean negativos
    def clean_precio(self):
        precio = self.cleaned_data.get('precio')
        if precio is not None and precio < 0:
            raise ValidationError('El precio no puede ser un número negativo.')
        return precio

    def clean_stock(self):
        stock = self.cleaned_data.get('stock')
        if stock is not None and stock < 0:
            raise ValidationError('El stock no puede ser un número negativo.')
        return stock
    
    def clean_precio_oferta(self):
        precio_oferta = self.cleaned_data.get('precio_oferta')
        if precio_oferta is not None and precio_oferta < 0:
            raise ValidationError('El precio de oferta no puede ser un número negativo.')
        return precio_oferta

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre', 'slug', 'descripcion']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


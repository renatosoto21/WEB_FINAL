from django import forms
from django.contrib.auth.models import User
from .models import Perfil
from django.core.exceptions import ValidationError

class RegistroUsuarioForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), label="Contraseña")
    password_confirm = forms.CharField(widget=forms.PasswordInput(), label="Confirmar Contraseña")

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
        labels = {
            'username': 'Nombre de usuario',
            'email': 'Correo electrónico',
            'first_name': 'Nombre',
            'last_name': 'Apellido',
        } 

    # Validamos que ambas contraseñas coincidan
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")
        if password != password_confirm:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        return cleaned_data

    # Guardamos encriptando la contraseña
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
    
    def verificar_email(self):
        email = self.cleaned_data.get('email')
        # Verificamos si escribieron algo y si NO termina en @gmail.com
        if email and not email.endswith('@gmail.com'):
            # Si no es gmail, detenemos el registro y lanzamos un error en la pantalla
            raise ValidationError('Solo se permiten cuentas de @gmail.com en esta tienda.')
        return email
    
# Formulario para actualizar los datos básicos
class UsuarioUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        labels = {
            'username': 'Nombre de usuario',
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'email': 'Correo electrónico',

        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control text-white', 'style': 'background-color: #2a2a2a; border: 1px solid #444;'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control text-white', 'style': 'background-color: #2a2a2a; border: 1px solid #444;'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control text-white', 'style': 'background-color: #2a2a2a; border: 1px solid #444;'}),
            'email': forms.EmailInput(attrs={'class': 'form-control text-white', 'style': 'background-color: #2a2a2a; border: 1px solid #444;'}),
        }
        help_texts = {
            'username': None,
        }

# Formulario exclusivo para subir la foto
class PerfilUpdateForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ['foto_perfil']
        labels = {
            'foto_perfil': 'Foto de Perfil',
        }
        widgets = {
            # Al usar FileInput en lugar del que viene por defecto, desaparece el texto "Currently / Change"
            'foto_perfil': forms.FileInput(attrs={'class': 'form-control text-white', 'style': 'background-color: #2a2a2a; border: 1px solid #444;'}),
        }
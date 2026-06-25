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
        
        labels = {'username': 'Nombre de usuario','email': 'Correo electrónico','first_name': 'Nombre','last_name': 'Apellido',} 

    # Validamos que ambas contraseñas coincidan
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")
        if password != password_confirm:
            self.add_error('password_confirm', "Las contraseñas no coinciden.")
            
        return cleaned_data


    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
    
#verificacion de los caractares minimos.
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and not email.endswith('@gmail.com'):
            raise ValidationError('Solo se permiten registrar cuentas de @gmail.com.')
        return email
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username and len(username) < 5:
            raise ValidationError('El nombre de usuario debe tener al menos 5 caracteres.')
        return username
    
    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if first_name and len(first_name) < 2:
            raise ValidationError('El nombre debe tener al menos 2 caracteres.')
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if last_name and len(last_name) < 2:
            raise ValidationError('El apellido debe tener al menos 2 caracteres.')
        return last_name
    
    def clean_password(self):
        password = self.cleaned_data.get('password')
        if password and len(password) < 6:
            raise ValidationError('La contraseña debe tener al menos 6 caracteres.')
        return password
    
# Formulario para actualizar los datos básicos
class UsuarioUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        labels = {'username': 'Nombre de usuario','first_name': 'Nombre','last_name': 'Apellido','email': 'Correo electrónico',} 

        widgets = {'username': forms.TextInput(attrs={'class': 'form-control text-white', 'style': 'background-color: #2a2a2a; border: 1px solid #444;'}),
                'first_name': forms.TextInput(attrs={'class': 'form-control text-white', 'style': 'background-color: #2a2a2a; border: 1px solid #444;'}),
                'last_name': forms.TextInput(attrs={'class': 'form-control text-white', 'style': 'background-color: #2a2a2a; border: 1px solid #444;'}),
                'email': forms.EmailInput(attrs={'class': 'form-control text-white', 'style': 'background-color: #2a2a2a; border: 1px solid #444;'})}
        
        help_texts = {
            'username': None,}

        
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")
        if password != password_confirm:
            self.add_error('password_confirm', "Las contraseñas no coinciden.")     
        return cleaned_data
    

    def save(self, commit=True):
        user = super().save(commit=False)
        nueva_contrasena = self.cleaned_data.get("password")
        if nueva_contrasena:
            user.set_password(nueva_contrasena)
        if commit:
            user.save()
        return user

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and not email.endswith('@gmail.com'):
            raise ValidationError('Solo se permiten registrar cuentas de @gmail.com.')
        return email
    

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username and len(username) < 5:
            raise ValidationError('El nombre de usuario debe tener al menos 5 caracteres.')
        return username
    

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if first_name and len(first_name) < 2:
            raise ValidationError('El nombre debe tener al menos 2 caracteres.')
        return first_name


    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if last_name and len(last_name) < 2:
            raise ValidationError('El apellido debe tener al menos 2 caracteres.')
        return last_name
    

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if password and len(password) < 6:
            raise ValidationError('La contraseña debe tener al menos 6 caracteres.')
        return password

# para subir la foto
class PerfilUpdateForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ['foto_perfil']
        labels = {'foto_perfil': 'Foto de Perfil',}
        widgets = {'foto_perfil': forms.FileInput(attrs={'class': 'form-control text-white', 'style': 'background-color: #2a2a2a; border: 1px solid #444;'})}
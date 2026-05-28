from django import forms
from django.contrib.auth.models import User

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
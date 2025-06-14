from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Libro

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control form-control-lg', 'placeholder': 'Nombre de usuario'})
        self.fields['password'].widget.attrs.update({'class': 'form-control form-control-lg', 'placeholder': 'Contraseña'})

class LibroForm(forms.ModelForm):
    class Meta:
        model = Libro
        fields = ['nombre', 'autor', 'genero', 'stock', 'portada_url'] # ¡Cambia 'portada' por 'portada_url'!
        # O si es un campo TextField para la URL
        widgets = {
            'portada_url': forms.URLInput(attrs={'placeholder': 'Ej: https://ejemplo.com/imagen.jpg'}),
        }
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.

class Libro(models.Model):
    """Modelo para representar un libro."""
    nombre = models.CharField(max_length=200)
    autor = models.CharField(max_length=200)
    genero = models.CharField(max_length=50)
    stock = models.IntegerField(default=1)
    portada_url = models.URLField(
        max_length=500,  # Un tamaño generoso para la URL
        null=True,
        blank=True,
        verbose_name='URL de la Portada del libro'
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    @property
    def disponibilidad(self):
        return self.stock > 0

    def __str__(self):
        return self.nombre
    
class Usuario(models.Model):
    """Modelo para representar un usuario."""
    nombre = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=50)
    fecha_registro = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.nombre

class PerfilUsuario(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    # Puedes agregar campos adicionales aquí si los necesitas en el futuro

    def __str__(self):
        return self.usuario.username
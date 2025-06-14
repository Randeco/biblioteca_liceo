from django.contrib import admin
from .models import Libro
from .models import PerfilUsuario

# Register your models here.
admin.site.register(Libro)
class LibroAdmin(admin.ModelAdmin):
    list_display = ('nombre','autor','mostrar_portada')
    leadonly_fields=('mostrar_portada',)

def mostrar_portada(self,obj):
    if obj.portada:
        return f'<img src="{obj.portada.url}" width="100" />'
    return "Sin portada"
mostrar_portada.allow_tags = True


admin.site.register(PerfilUsuario)
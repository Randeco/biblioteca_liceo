# prestamos/urls.py

from django.urls import path
from . import views

app_name = 'prestamos'  # Importante: Define el namespace de la app

urlpatterns = [
    path('', views.lista_prestamos, name='lista_prestamos'),
    path('crear/', views.crear_prestamo, name='crear_prestamo'),
    path('editar/<int:prestamo_id>/', views.editar_prestamo, name='editar_prestamo'),
    path('eliminar/<int:prestamo_id>/', views.eliminar_prestamo, name='eliminar_prestamo'),
]
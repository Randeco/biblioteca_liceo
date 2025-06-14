# libros/urls.py
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.lista_libros, name='lista_libros'),
    path('buscar/', views.buscar_libros, name='buscar_libros'),
    path('dashboard/', views.usuario_dashboard, name='usuario_dashboard'),
    path('libros/crear/', views.crear_libro, name='crear_libro'),  # Nueva URL para crear libros
    path('editar/<int:libro_id>/', views.editar_libro, name='editar_libro'),
    path('libros/eliminar/<int:libro_id>/', views.eliminar_libro, name='eliminar_libro'),
    path('libros/detalles/<int:libro_id>/', views.detalles_libro, name='detalles_libro'),
]
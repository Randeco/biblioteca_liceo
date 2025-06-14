"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from libros import views# Importa las vistas del proyecto si tienes alguna AQUI
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('libros/', include('libros.urls')), # Incluye las URLs de la app libros bajo el prefijo /libros/
    path('', views.home, name='home'), # Asegúrate de que 'home' esté importado correctamente (aquí asumo que está en las vistas del proyecto)
    path('reservar/<int:libro_id>/', views.reservar_libro, name='reservar_libro'), # Asegúrate de que 'reservar_libro' esté importado correctamente
    path('libros/login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('prestamos/', include('prestamos.urls')),
    # La ruta 'buscar/' ya está definida en libros/urls.py
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

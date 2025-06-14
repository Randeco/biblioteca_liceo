from django.shortcuts import render
from .models import Libro
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import LibroForm

# Create your views here.
def lista_libros(request):
    libros = Libro.objects.all()
    return render(request, 'libros/lista.html', {'libros': libros})

def home(request):
    libros_destacados = Libro.objects.order_by('-fecha_creacion')[:5]
    return render(request, 'libros/home.html', {'libros_destacados': libros_destacados})

def reservar_libro(request, libro_id):
    libro = get_object_or_404(Libro, id=libro_id)
    return render(request, 'libros/reserva.html', {'libro': libro})

@login_required
def vista_protegida(request):
    return render(request, 'templates_protegido.html')

def buscar_libros(request):
    query = request.GET.get('q')
    resultados = []

    if query:
        resultados = Libro.objects.filter(
            Q(nombre__icontains=query) |
            Q(autor__icontains=query) |
            Q(genero__icontains=query)
        ).distinct() # Añadí .distinct() para evitar duplicados si un libro coincide en varios campos
    else:
        resultados = Libro.objects.all() # Si no hay búsqueda, obtenemos todos los libros

    return render(request, 'libros/lista.html', {'libros': resultados, 'query': query})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('usuario_dashboard')  # Redirige a tu dashboard
            else:
                messages.error(request, "Nombre de usuario o contraseña incorrectos.")
        else:
            messages.error(request, "Nombre de usuario o contraseña incorrectos.")
    else:
        form = AuthenticationForm()
    return render(request, 'libros/login.html', {'form': form})

@login_required
def usuario_dashboard(request):
    libros = Libro.objects.all()  # Consulta todos los libros de la base de datos inicialmente
    query = request.GET.get('q')
    if query:
        libros = libros.filter(
            Q(nombre__icontains=query) |
            Q(autor__icontains=query) |
            Q(genero__icontains=query)
        )
    response = render(request, 'libros/usuario_dashboard.html', {'libros': libros}) # Pasa la lista de libros (filtrada o no) al template
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response

@login_required
def crear_libro(request):
    print("Solicitud CREAR libro recibida:", request.method)
    print("Datos POST (crear):", request.POST)
    print("Archivos FILES (crear):", request.FILES) # Esto ya no debería tener nada para la portada
    if request.method == 'POST':
        # La clave está en cómo LibroForm maneja la 'portada'
        form = LibroForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('usuario_dashboard')
        else:
            # Manejar errores del formulario si es necesario
            # print("Errores del formulario (crear):", form.errors) # Puedes descomentar esto para depurar
            return redirect('usuario_dashboard')
    else:
        return redirect('usuario_dashboard')

@login_required
def editar_libro(request, libro_id):
    print("Solicitud EDITAR libro recibida:", request.method, "ID:", libro_id)
    print("Datos POST (editar):", request.POST)
    print("Archivos FILES (editar):", request.FILES) # Esto ya no debería tener nada para la portada
    libro = get_object_or_404(Libro, id=libro_id)
    if request.method == 'POST':
        # La clave está en cómo LibroForm maneja la 'portada'
        form = LibroForm(request.POST, request.FILES, instance=libro)
        if form.is_valid():
            form.save()
            return redirect('usuario_dashboard')
        else:
            # Manejar errores del formulario si es necesario
            # print("Errores del formulario (editar):", form.errors) # Puedes descomentar esto para depurar
            return redirect('usuario_dashboard')
    else:
        return redirect('usuario_dashboard')
    
@login_required
def eliminar_libro(request, libro_id):
    libro = get_object_or_404(Libro, id=libro_id)
    if request.method == 'POST':
        libro.delete()
        return redirect('usuario_dashboard')
    return redirect('usuario_dashboard')



@login_required
def detalles_libro(request, libro_id):
    libro = get_object_or_404(Libro, id=libro_id)
    return render(request, 'libros/detalles_libro.html', {'libro': libro})
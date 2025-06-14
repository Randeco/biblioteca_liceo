# prestamos/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Prestamo, Libro # Asegúrate de importar Libro
from .forms import PrestamoForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.db.models import Q
from .forms import PrestamoForm
from django.views.decorators.http import require_POST


@login_required
def lista_prestamos(request):
    query = request.GET.get('q')

    prestamos = Prestamo.objects.all()

    if query:
        prestamos = prestamos.filter(
            Q(libro__nombre__icontains=query) |
            Q(nombre_persona__icontains=query) |
            Q(rut__icontains=query)
        ).distinct()

    # --- ESTAS DOS LÍNEAS SON LA CLAVE PARA EL MODAL "NUEVO PRÉSTAMO" ---
    # 1. Crea una instancia vacía de tu formulario de préstamo.
    form = PrestamoForm() 

    context = {
        'prestamos': prestamos,
        'query': query,
        # 2. Pasa esa instancia del formulario al contexto de la plantilla.
        'form': form, 
    }
    return render(request, 'prestamos/lista_prestamos.html', context)

@require_POST
@login_required
def crear_prestamo(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        form = PrestamoForm(request.POST)
        if form.is_valid():
            prestamo = form.save(commit=False)
            if prestamo.libro.stock > 0:
                prestamo.libro.stock -= 1
                prestamo.libro.save()
                prestamo.save()

                prestamo_data = {
                    'id': prestamo.id,
                    'libro': prestamo.libro.nombre,
                    'nombre_persona': prestamo.nombre_persona,
                    'curso': prestamo.curso,
                    'rut': prestamo.rut,
                    'celular': prestamo.celular,
                    'fecha_prestamo': prestamo.fecha_prestamo.strftime('%Y-%m-%d'),
                    'fecha_devolucion': prestamo.fecha_devolucion.strftime('%Y-%m-%d') if prestamo.fecha_devolucion else 'Pendiente',
                }
                return JsonResponse({'success': True, 'prestamo': prestamo_data})
            else:
                # Error de stock
                return JsonResponse({'success': False, 'errors': {'libro': ['No hay stock disponible para este libro.']}}, status=400)
        else:
            # --- ¡LA CORRECCIÓN ESTÁ AQUÍ! ---
            # Convierte form.errors a un formato serializable a JSON
            # form.errors.as_json() devolverá una cadena JSON
            return JsonResponse({'success': False, 'errors': form.errors.as_json()}, status=400) # Estado 400 para indicar un error de cliente (Bad Request)
    else:
        # Si la petición no es AJAX
        return JsonResponse({'success': False, 'error': 'Petición inválida. Solo se permiten peticiones AJAX POST.'}, status=400)


@login_required
def editar_prestamo(request, prestamo_id):
    prestamo = get_object_or_404(Prestamo, pk=prestamo_id)

    if request.method == 'GET' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        form = PrestamoForm(instance=prestamo)
        form_html = render_to_string('prestamos/form_editar_prestamo.html', {'form': form}, request=request)
        return JsonResponse({'success': True, 'form_html': form_html})

    elif request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        form = PrestamoForm(request.POST, instance=prestamo)
        if form.is_valid():
            old_prestamo = Prestamo.objects.get(pk=prestamo_id)
            
            # Lógica de manejo de stock si el libro cambia
            if old_prestamo.libro != form.cleaned_data['libro']:
                old_prestamo.libro.stock += 1 # Devuelve el libro viejo al stock
                old_prestamo.libro.save()
                
                new_libro = form.cleaned_data['libro']
                if new_libro.stock > 0:
                    new_libro.stock -= 1 # Toma el nuevo libro del stock
                    new_libro.save()
                else:
                    form.add_error('libro', 'No hay stock disponible para el nuevo libro seleccionado.')
                    return JsonResponse({'success': False, 'errors': form.errors})
            
            prestamo_actualizado = form.save()

            prestamo_data = {
                'id': prestamo_actualizado.id,
                'libro': prestamo_actualizado.libro.nombre,
                'nombre_persona': prestamo_actualizado.nombre_persona,
                'curso': prestamo_actualizado.curso,
                'rut': prestamo_actualizado.rut,
                'celular': prestamo_actualizado.celular,
                'fecha_prestamo': prestamo_actualizado.fecha_prestamo.strftime('%Y-%m-%d'),
                'fecha_devolucion': prestamo_actualizado.fecha_devolucion.strftime('%Y-%m-%d') if prestamo_actualizado.fecha_devolucion else 'Pendiente',
                # 'devuelto': prestamo_actualizado.devuelto, # <--- CAMBIO: Eliminado
            }
            return JsonResponse({'success': True, 'prestamo': prestamo_data})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        return JsonResponse({'success': False, 'error': 'Petición inválida'})

@login_required
def eliminar_prestamo(request, prestamo_id):
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        try:
            prestamo = get_object_or_404(Prestamo, pk=prestamo_id)
            libro = prestamo.libro
            prestamo.delete()
            libro.stock += 1 # Incrementar el stock cuando un préstamo se elimina
            libro.save()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid request method or not AJAX'})
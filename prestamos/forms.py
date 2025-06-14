# prestamos/forms.py
from django import forms
from .models import Prestamo
from libros.models import Libro
import re

class PrestamoForm(forms.ModelForm):
    class Meta:
        model = Prestamo
        fields = ['libro', 'nombre_persona', 'curso', 'rut', 'celular', 'fecha_devolucion']
        widgets = {
            # Aquí se define el widget para fecha_devolucion y se añaden los placeholders
            'fecha_devolucion': forms.DateInput(attrs={'type': 'date', 'placeholder': 'AAAA-MM-DD'}),
            'nombre_persona': forms.TextInput(attrs={'placeholder': 'Ej: Juan Pérez'}),
            'rut': forms.TextInput(attrs={'placeholder': 'Ej: 12345678-9'}),
            'celular': forms.TextInput(attrs={'placeholder': 'Ej: 912345678'}), # O el formato que esperes
            # 'curso': forms.TextInput(attrs={'placeholder': 'Ej: 3ro Básico'}) # Puedes añadirlo si es un TextInput
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Solo mostrar libros con stock > 0
        self.fields['libro'].queryset = Libro.objects.filter(stock__gt=0)
        self.fields['libro'].label = 'Libro a prestar'
        self.fields['nombre_persona'].label = 'Nombre del solicitante'
        self.fields['curso'].label = 'Curso'
        self.fields['rut'].label = 'RUT'
        self.fields['celular'].label = 'Celular'
        self.fields['fecha_devolucion'].label = 'Fecha de devolución (opcional)'

    def clean_rut(self):
        rut = self.cleaned_data['rut']
        rut_limpio_para_validacion = rut.replace(".", "").replace("-", "").upper()

        if not re.match(r'^\d{7,8}[0-9K]$', rut_limpio_para_validacion):
            raise forms.ValidationError("El formato del RUT no es válido. Debe ser Ej: 12.345.678-9 o 12345678-9.")

        cuerpo_rut = rut_limpio_para_validacion[:-1]
        dv_ingresado = rut_limpio_para_validacion[-1]

        suma = 0
        multiplicador = 2
        for digito in reversed(cuerpo_rut):
            suma += int(digito) * multiplicador
            multiplicador += 1
            if multiplicador == 8:
                multiplicador = 2
        
        dv_calculado = 11 - (suma % 11)
        if dv_calculado == 11:
            dv_calculado = '0'
        elif dv_calculado == 10:
            dv_calculado = 'K'
        else:
            dv_calculado = str(dv_calculado)

        if dv_ingresado != dv_calculado:
            raise forms.ValidationError("El RUT ingresado no es válido.")
            
        rut_final_formateado = f"{cuerpo_rut}-{dv_ingresado}"
        
        return rut_final_formateado
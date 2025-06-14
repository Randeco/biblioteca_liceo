# prestamos/models.py
from django.db import models
from libros.models import Libro

class Prestamo(models.Model):
    # ¡LISTA FINAL Y ORDENADA DE CURSOS Y CATEGORÍAS!
    # Formato: (valor_a_guardar_en_bd, nombre_a_mostrar_en_formulario_y_en_tabla)
    CURSO_CHOICES = [
        # Cursos Generales (1° y 2°)
        ('1A', '1° A'),
        ('1B', '1° B'),
        ('1C', '1° C'),
        ('1D', '1° D'),
        ('1E', '1° E'),
        ('1F', '1° F'),
        ('1G', '1° G'),
        ('2A', '2° A'),
        ('2B', '2° B'),
        ('2C', '2° C'),
        ('2D', '2° D'),
        ('2E', '2° E'),
        ('2F', '2° F'),
        ('2G', '2° G'),
        
        # Cursos Humanístico-Científicos (H.C.)
        ('3HC', '3° H.C.'),
        ('4HC', '4° H.C.'),

        # Carreras Técnicas / Especialidades (3° y 4°)
        ('3CM', '3° Construcciones Metálicas'),
        ('4CM', '4° Construcciones Metálicas'),
        ('3MI', '3° Mecánica Industrial'),
        ('4MI', '4° Mecánica Industrial'), 
        ('3EL', '3° Electricidad'),
        ('4EL', '4° Electricidad'),
        ('3ELE', '3° Electrónica'),
        ('4ELE', '4° Electrónica'),
        ('3ENF', '3° Enfermería'),
        ('4ENF', '4° Enfermería'),
        ('3GAS', '3° Gastronomía'),
        ('4GAS', '4° Gastronomía'),
        ('3EDI', '3° Edificación'),
        ('4EDI', '4° Edificación'),

        # Talleres Laborales
        ('TALLER_1', 'Taller Laboral 1'),
        ('TALLER_2', 'Taller Laboral 2'),
        
        # Categorías de Personal
        ('FUNCIONARIO', 'Funcionario'),
    ]

    libro = models.ForeignKey(Libro, on_delete=models.CASCADE)
    nombre_persona = models.CharField(max_length=200)
    
    curso = models.CharField(
        max_length=50,
        choices=CURSO_CHOICES,
        default='OTROS', # Puedes mantener 'OTROS' como valor por defecto o cambiarlo
    )
    
    rut = models.CharField(max_length=12)
    celular = models.CharField(max_length=15)
    fecha_prestamo = models.DateField(auto_now_add=True)
    fecha_devolucion = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Préstamo de {self.libro.nombre} a {self.nombre_persona}"
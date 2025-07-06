from django.db import models
from django.contrib.auth.models import User
from datetime import date

ESTADOS = [
    ('pendiente', 'Pendiente'),
    ('aceptado', 'Aceptado'),
    ('rechazado', 'Rechazado'),
]

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()

    def __str__(self):
        return self.nombre

class Lugar(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre

class Profesor(models.Model):
    nombre_completo = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre_completo

class Taller(models.Model):
    titulo = models.CharField(max_length=200)
    fecha = models.DateField()
    duracion_horas = models.FloatField()
    estado = models.CharField(max_length=10, choices=ESTADOS, default='pendiente')
    observacion = models.TextField(blank=True, null=True)

    profesor = models.ForeignKey(Profesor, on_delete=models.CASCADE)
    lugar = models.ForeignKey(Lugar, on_delete=models.CASCADE)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    creado_por = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.titulo

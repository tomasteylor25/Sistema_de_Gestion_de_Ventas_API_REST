"""App Clientes"""

from django.db import models
from api.models_base import ModeloBase


class Cliente(ModeloBase):
    TIPO_DOCUMENTO = [
        ('CC', 'Cédula de Ciudadanía'),
        ('NIT', 'NIT'),
        ('CE', 'Cédula Extranjería'),
        ('PP', 'Pasaporte'),
    ]
    tipo_documento  = models.CharField(max_length=5, choices=TIPO_DOCUMENTO, default='CC')
    numero_documento = models.CharField(max_length=20, unique=True)
    nombre          = models.CharField(max_length=150)
    apellido        = models.CharField(max_length=150, blank=True)
    email           = models.EmailField(unique=True)
    telefono        = models.CharField(max_length=20, blank=True)
    direccion       = models.TextField(blank=True)
    ciudad          = models.CharField(max_length=100, blank=True)

    class Meta:
        db_table = 'clientes'
        ordering = ['nombre']

    def __str__(self):
        return f'{self.nombre} {self.apellido} ({self.numero_documento})'

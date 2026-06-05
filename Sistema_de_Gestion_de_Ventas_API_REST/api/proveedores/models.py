from django.db import models
from api.models_base import ModeloBase


class Proveedor(ModeloBase):
    nit          = models.CharField(max_length=20, unique=True)
    nombre       = models.CharField(max_length=200)
    contacto     = models.CharField(max_length=150, blank=True)
    email        = models.EmailField(blank=True)
    telefono     = models.CharField(max_length=20, blank=True)
    direccion    = models.TextField(blank=True)
    ciudad       = models.CharField(max_length=100, blank=True)
    sitio_web    = models.URLField(blank=True)

    class Meta:
        db_table = 'proveedores'
        ordering = ['nombre']

    def __str__(self):
        return f'{self.nombre} ({self.nit})'

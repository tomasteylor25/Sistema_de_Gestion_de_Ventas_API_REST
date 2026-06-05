from django.db import models
from api.models_base import ModeloBase


class Sucursal(ModeloBase):
    codigo     = models.CharField(max_length=20, unique=True)
    nombre     = models.CharField(max_length=200)
    direccion  = models.TextField()
    ciudad     = models.CharField(max_length=100)
    telefono   = models.CharField(max_length=20, blank=True)
    email      = models.EmailField(blank=True)
    es_principal = models.BooleanField(default=False)

    class Meta:
        db_table = 'sucursales'
        ordering = ['nombre']

    def __str__(self):
        return f'{self.nombre} - {self.ciudad}'

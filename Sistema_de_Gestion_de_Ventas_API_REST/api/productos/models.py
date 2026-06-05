from django.db import models
from api.models_base import ModeloBase
from api.proveedores.models import Proveedor


class Producto(ModeloBase):
    UNIDAD_MEDIDA = [
        ('UND', 'Unidad'),
        ('KG',  'Kilogramo'),
        ('LT',  'Litro'),
        ('MT',  'Metro'),
        ('CJ',  'Caja'),
    ]
    codigo        = models.CharField(max_length=50, unique=True)
    nombre        = models.CharField(max_length=200)
    descripcion   = models.TextField(blank=True)
    precio        = models.DecimalField(max_digits=12, decimal_places=2)
    stock         = models.IntegerField(default=0)
    stock_minimo  = models.IntegerField(default=5)
    unidad_medida = models.CharField(max_length=5, choices=UNIDAD_MEDIDA, default='UND')
    proveedor     = models.ForeignKey(
        Proveedor,
        on_delete=models.PROTECT,
        related_name='productos'
    )

    class Meta:
        db_table = 'productos'
        ordering = ['nombre']

    def __str__(self):
        return f'{self.nombre} ({self.codigo})'

    @property
    def stock_bajo(self):
        return self.stock <= self.stock_minimo

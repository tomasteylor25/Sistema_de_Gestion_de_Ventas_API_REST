from django.db import models
from api.models_base import ModeloBase
from api.pedidos.models import Pedido


class Factura(ModeloBase):
    ESTADO = [
        ('PENDIENTE', 'Pendiente'),
        ('PAGADA',    'Pagada'),
        ('ANULADA',   'Anulada'),
        ('VENCIDA',   'Vencida'),
    ]
    numero_factura = models.CharField(max_length=20, unique=True)
    fecha_emision  = models.DateField()
    fecha_vencimiento = models.DateField()
    estado         = models.CharField(max_length=10, choices=ESTADO, default='PENDIENTE')
    pedido         = models.OneToOneField(
        Pedido, on_delete=models.PROTECT, related_name='factura'
    )
    subtotal       = models.DecimalField(max_digits=14, decimal_places=2)
    iva            = models.DecimalField(max_digits=5,  decimal_places=2, default=19)
    total          = models.DecimalField(max_digits=14, decimal_places=2)
    observaciones  = models.TextField(blank=True)

    class Meta:
        db_table = 'facturas'
        ordering = ['-fecha_emision']

    def save(self, *args, **kwargs):
        self.total = self.subtotal * (1 + self.iva / 100)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Factura {self.numero_factura}'

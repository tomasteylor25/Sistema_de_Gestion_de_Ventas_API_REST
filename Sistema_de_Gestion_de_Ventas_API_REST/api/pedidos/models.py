from django.db import models
from api.models_base import ModeloBase
from api.clientes.models import Cliente
from api.sucursales.models import Sucursal


class Pedido(ModeloBase):
    ESTADO = [
        ('PENDIENTE',  'Pendiente'),
        ('APROBADO',   'Aprobado'),
        ('ENVIADO',    'Enviado'),
        ('ENTREGADO',  'Entregado'),
        ('CANCELADO',  'Cancelado'),
    ]
    numero_pedido  = models.CharField(max_length=20, unique=True)
    fecha_pedido   = models.DateField()
    fecha_entrega  = models.DateField(null=True, blank=True)
    estado         = models.CharField(max_length=15, choices=ESTADO, default='PENDIENTE')
    cliente        = models.ForeignKey(
        Cliente, on_delete=models.PROTECT, related_name='pedidos'
    )
    sucursal       = models.ForeignKey(
        Sucursal, on_delete=models.PROTECT, related_name='pedidos'
    )
    observaciones  = models.TextField(blank=True)
    total          = models.DecimalField(max_digits=14, decimal_places=2, default=0)

    class Meta:
        db_table = 'pedidos'
        ordering = ['-fecha_pedido']

    def __str__(self):
        return f'Pedido {self.numero_pedido} - {self.cliente}'

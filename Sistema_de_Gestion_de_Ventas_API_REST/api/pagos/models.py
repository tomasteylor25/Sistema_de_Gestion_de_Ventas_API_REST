from django.db import models
from api.models_base import ModeloBase
from api.facturas.models import Factura


class Pago(ModeloBase):
    METODO = [
        ('EFECTIVO',       'Efectivo'),
        ('TRANSFERENCIA',  'Transferencia Bancaria'),
        ('TARJETA_CRED',   'Tarjeta de Crédito'),
        ('TARJETA_DEB',    'Tarjeta de Débito'),
        ('CHEQUE',         'Cheque'),
        ('PSE',            'PSE'),
    ]
    ESTADO = [
        ('PENDIENTE',  'Pendiente'),
        ('APROBADO',   'Aprobado'),
        ('RECHAZADO',  'Rechazado'),
        ('REEMBOLSADO','Reembolsado'),
    ]
    numero_pago      = models.CharField(max_length=20, unique=True)
    fecha_pago       = models.DateField()
    monto            = models.DecimalField(max_digits=14, decimal_places=2)
    metodo_pago      = models.CharField(max_length=15, choices=METODO)
    estado           = models.CharField(max_length=12, choices=ESTADO, default='PENDIENTE')
    referencia       = models.CharField(max_length=100, blank=True,
                                        help_text='Número de transacción o referencia bancaria')
    factura          = models.ForeignKey(
        Factura, on_delete=models.PROTECT, related_name='pagos'
    )
    observaciones    = models.TextField(blank=True)

    class Meta:
        db_table = 'pagos'
        ordering = ['-fecha_pago']

    def __str__(self):
        return f'Pago {self.numero_pago} - {self.monto} ({self.get_estado_display()})'

from django.db import models
from django.core.validators import MinValueValidator
from api.models_base import ModeloBase
from api.pedidos.models import Pedido
from api.productos.models import Producto


class DetallePedido(ModeloBase):
    pedido      = models.ForeignKey(
        Pedido, on_delete=models.CASCADE, related_name='detalles'
    )
    producto    = models.ForeignKey(
        Producto, on_delete=models.PROTECT, related_name='detalles_pedido'
    )
    cantidad    = models.IntegerField(validators=[MinValueValidator(1)])
    precio_unitario = models.DecimalField(max_digits=12, decimal_places=2)
    descuento   = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    subtotal    = models.DecimalField(max_digits=14, decimal_places=2, editable=False, default=0)

    class Meta:
        db_table = 'detalle_pedidos'
        unique_together = ['pedido', 'producto']

    def save(self, *args, **kwargs):
        self.subtotal = self.cantidad * self.precio_unitario * (1 - self.descuento / 100)
        super().save(*args, **kwargs)
        # Actualizar total del pedido
        from django.db.models import Sum
        total = self.pedido.detalles.aggregate(total=Sum('subtotal'))['total'] or 0
        Pedido.objects.filter(pk=self.pedido_id).update(total=total)

    def __str__(self):
        return f'{self.producto.nombre} x{self.cantidad} en pedido {self.pedido.numero_pedido}'

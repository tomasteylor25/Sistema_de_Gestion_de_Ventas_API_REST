from django.contrib import admin
from .models import DetallePedido


@admin.register(DetallePedido)
class DetallePedidoAdmin(admin.ModelAdmin):
    list_display    = ['pedido', 'producto', 'cantidad', 'precio_unitario', 'descuento', 'subtotal', 'activo']
    list_filter     = ['activo']
    search_fields   = ['pedido__numero_pedido', 'producto__nombre']
    raw_id_fields   = ['pedido', 'producto']
    readonly_fields = ['subtotal']

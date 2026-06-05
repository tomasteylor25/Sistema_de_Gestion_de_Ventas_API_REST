from django.contrib import admin
from .models import Pedido
from api.detalle_pedidos.models import DetallePedido


class DetallePedidoInline(admin.TabularInline):
    model  = DetallePedido
    extra  = 1
    fields = ['producto', 'cantidad', 'precio_unitario', 'descuento', 'subtotal', 'activo']
    readonly_fields = ['subtotal']


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display  = ['numero_pedido', 'cliente', 'sucursal', 'estado', 'total', 'fecha_pedido', 'activo']
    list_filter   = ['estado', 'sucursal', 'activo']
    search_fields = ['numero_pedido', 'cliente__nombre', 'cliente__numero_documento']
    ordering      = ['-fecha_pedido']
    raw_id_fields = ['cliente', 'sucursal']
    inlines       = [DetallePedidoInline]
    readonly_fields = ['total']
